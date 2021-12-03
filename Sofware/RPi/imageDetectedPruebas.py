import numpy as np
import cv2
from datetime import date
from datetime import datetime
import os
from picamera import PiCamera
from time import sleep
import os
import time
import RPi.GPIO as GPIO
from time import sleep

camera = PiCamera()

bandera=True

print(time.strftime("%M"))


fecha=time.strftime("%d-%m-%y")
minutos=time.strftime("%M")
       
if str(minutos) != "50":
       bandera=True
              
if (bandera==True):  
       
       now = datetime.now()

       os.mkdir(str(now))

       fecha=time.strftime("%d-%m-%y")
       hora=time.strftime("%H:%M:%S")
       direccionCarpeta='/home/pi/ProcesamientoCoordinoscopio/'+str(now)+'/'
       
       
       GPIO.setmode(GPIO.BCM)
       GPIO.setwarnings(False)
       GPIO.setup(12, GPIO.OUT)

#GPIO.output(12, GPIO.HIGH)

       pwm = GPIO.PWM(12, 100)
       pwm.start(100)
       
       ##########################-Captura de Imagen-###########################
       ########################################################################

       camera.resolution= (600,300)
       #camera.rotation = 180
       camera.start_preview()
       camera.capture(direccionCarpeta+str(fecha)+str(hora)+'.jpeg')
       sleep(1)
       camera.zoom = (0.30, 0.5, 0.4, 0.4)
       sleep(1)
       camera.capture(direccionCarpeta+str(fecha)+str(hora)+'x2.jpeg')
       camera.stop_preview()
       sleep(1)
       
       pwm.stop()
       
       ####################-Procesamiento de Imagen-##########################
       #######################################################################

       img = cv2.imread(direccionCarpeta+str(fecha)+str(hora)+'x2.jpeg')
       #img = cv2.imread('fotoprueba7Zoom.jpeg')
       height, width = img.shape[:2]
       
       #res = cv2.resize(img,(4*width, 4*height), interpolation = cv2.INTER_CUBIC)
       #cv2.imwrite(direccionCarpeta+str(fecha)+str(hora)+'zoomx4.jpg',res)

       #gray = cv2.imread(direccionCarpeta+str(fecha)+str(hora)+'zoomx4.jpg')
       gray = cv2.imread(direccionCarpeta+str(fecha)+str(hora)+'x2.jpeg')
       edges = cv2.Canny(gray,0,2000,apertureSize = 5)
     
       cv2.imwrite(direccionCarpeta+str(fecha)+str(hora)+'edges.jpg',edges)
       minLineLength=200
       lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=80)

       a,b,c = lines.shape

       f = open(direccionCarpeta+str(fecha)+str(hora)+".csv","w")

       for i in range(a):
              cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
              print(lines[i][0][0], lines[i][0][1], lines[i][0][2], lines[i][0][3])
              f.write(str(lines[i][0][0])+"\t"+ str(lines[i][0][1])+"\t"+str(lines[i][0][2])+"\t"+str(lines[i][0][3])+"\n")
              cv2.imwrite(direccionCarpeta+str(fecha)+str(hora)+'houghlines2.jpg',gray)

       f.close
       bandera=False
              
