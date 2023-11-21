from datetime import date
from datetime import datetime
import os
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
from time import sleep

camera = PiCamera()
bandera=False

print(str(time.strftime("%H"))+":"+str(time.strftime("%M"))+":"+str(time.strftime("%S")))

def TomarFotografia(direccionCarpeta):
      
       now = datetime.now()       
       
       GPIO.setmode(GPIO.BCM)
       GPIO.setwarnings(False)
       GPIO.setup(12, GPIO.OUT)
#GPIO.output(12, GPIO.HIGH)
       pwm = GPIO.PWM(12, 100)
       pwm.start(100)
       sleep(1)
       try:
                            
       ##########################-Captura de Imagen-###########################
       ########################################################################
              camera.resolution= (600,300)
              #camera.rotation = 180
              camera.start_preview()
              #camera.capture(direccionCarpeta+'imagenSinZoom.jpeg')
              sleep(1)
              camera.zoom = (0.3, 0.5, 0.4, 0.4)
              sleep(1)
              imagenZoomx2 = direccionCarpeta +str(now)+'.jpg'
              camera.capture(imagenZoomx2)
              camera.stop_preview()
              sleep(1)
              pwm.stop()   
       except:
              print("No se puede capturar la imagen")
              pwm.stop()
       
       return imagenZoomx2,now