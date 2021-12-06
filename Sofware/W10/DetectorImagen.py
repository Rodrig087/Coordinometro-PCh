import numpy as np
import cv2
from datetime import date
from datetime import datetime
import os


import os
import time


print(str(time.strftime("%H"))+":"+str(time.strftime("%M"))+":"+str(time.strftime("%S")))


#********************************** Metodos ***********************************

def ProcesarImagen(imagen, direccionCarpeta):
       
       mat_datos_x=[]
       puntoMenor=0
       
       try:
       ####################-Procesamiento de Imagen-##########################
       #######################################################################
              
              print (imagen)
              img = cv2.imread(imagen)
              height, width = img.shape[:2]
              #print("llego")
             
              gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
              gauss = cv2.medianBlur(gris,13)
              cv2.imwrite(direccionCarpeta+'filtroblur.jpg',gauss)
              canny = cv2.Canny(gauss, 100, 150)
              
              lines = cv2.HoughLinesP(image=canny,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=180,maxLineGap=100)
                     
              a,b,c = lines.shape

              f = open(direccionCarpeta+"datosMedidos.txt","a")

              for i in range(a):
                     cv2.line(gauss, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
                     print(lines[i][0][0], lines[i][0][1], lines[i][0][2], lines[i][0][3])
                     mat_datos_x.append(lines[i][0][0])
                     cv2.imwrite(direccionCarpeta+'lineasMarcadas.jpg',gauss)

              puntoMayor=max(mat_datos_x)
              puntoMenor=min(mat_datos_x)
              anchoCable=215
              relacionPixel=2/anchoCable
              print(anchoCable)
              print("Mayor: %d" % puntoMayor)
              print("Menor: %d" % puntoMenor)
              print(str(puntoMenor*relacionPixel)+' mm')
              
              mat_datos_x.clear()

             #f.write(str(horaFecha)+"\t"+str(puntoMenor)+"\t"+ str(puntoMayor)+"\t"+str(puntoMenor*relacionPixel)+"\n")
              f.write(str(puntoMenor)+"\t"+ str(puntoMayor)+"\t"+str(puntoMenor*relacionPixel)+"\n")
              f.close
              
              puntoMenor=0
              puntoMayor=0
       except:
              print("Imagen Mala para realizar el calculo")
              
#******************************************************************************


#************************************ Main ************************************

#direccionCarpeta = "C:/Users/Ivan/Desktop/Milton Muñoz/Proyectos/Proyecto Chanlud/Analisis/Coordinometros/Fotos/"
direccionCarpeta = "C:/Users/milto/Milton/RSA/Proyectos/Proyecto Chanlud/Analisis/Coordinometros/Fotos/"

nombreArchivo = input("Ingrese el nombre de la foto: ")

imagen = direccionCarpeta + nombreArchivo + ".jpg"
              
ProcesarImagen(imagen,direccionCarpeta)

#******************************************************************************
