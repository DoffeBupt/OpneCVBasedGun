import numpy as np
import cv2
import RPi.GPIO as GPIO
import time
import signal
import atexit

from sympy.vector import Point

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=False)
GPIO.setup(27, GPIO.OUT, initial=False)
p = GPIO.PWM(17,50) #50HZ
q = GPIO.PWM(27,50) #50HZ
p.start(0)
time.sleep(2)
pangle = 5
qangle = 5

while True:
    ret, img = cap.read()
    img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    cv2.putText(img, "x", (320, 240),(0, 255, 0))
    cv2.imshow('video',img)
    if (abs((x+w/2)-320)>15 or abs((y+h/2)-240)>15):
        if (x+w/2)<320:
            pangle = pangle + 0.03
        else:
            pangle = pangle - 0.03

        if (y+h/2)<240:
            pangle = pangle + 0.03
        else:
            pangle = pangle - 0.03

        p.ChangeDutyCycle(2.5+pangle)
        q.ChangeDutyCycle(2.5+qangle)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows()