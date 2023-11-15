import numpy as np
import cv2
from datetime import date
from datetime import datetime
import os
import time


#print(str(time.strftime("%H"))+":"+str(time.strftime("%M"))+":"+str(time.strftime("%S")))


#********************************** Metodos ***********************************

def ProcesarImagen(imagen, direccionCarpeta):
       
              mat_datos_x=[]
              puntoMenor=0
       
       #try:
       ####################-Procesamiento de Imagen-##########################
       #######################################################################
              
              '''
              tiempoImagen = imagen[54:73]  
              tiempoImagen_dt = datetime.strptime(tiempoImagen, '%Y-%m-%d %H_%M_%S')
              tiempoImagen_str = str(tiempoImagen_dt)
              print(tiempoImagen)
              print(tiempoImagen_dt)
             '''
              
              img = cv2.imread(imagen)
              height, width = img.shape[:2]
                           
              gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
              gauss = cv2.medianBlur(gris,13)
              cv2.imwrite(direccionCarpeta+'filtroblur.jpg',gauss)
              canny = cv2.Canny(gauss, 10, 30)
                            
              lines = cv2.HoughLinesP(image=canny,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=180,maxLineGap=100)
              a,b,c = lines.shape
              
              for i in range(a):
                     cv2.line(gauss, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 255, 0), 3, cv2.LINE_AA)
                     mat_datos_x.append(lines[i][0][0])
                     cv2.imwrite(direccionCarpeta+'lineasMarcadas.jpg',gauss)

              puntoMayor = max(mat_datos_x)
              puntoMenor = min(mat_datos_x)
              anchoCable = puntoMayor - puntoMenor
              relacionPixel = 2/anchoCable
              bordeMenor = puntoMenor*relacionPixel
              
              print("Borde menor [px]: %d" % puntoMenor)
              print("Borde mayor [px]: %d" % puntoMayor)
              print("Grosor del cable [px]: %d" % anchoCable)
              print("Relacion mm/px: %f" % relacionPixel)
              print("Posicion borde menor [mm]: %f" % (puntoMenor*relacionPixel))
              
              #print( tiempoImagen_str + "\t%d\t%d\t%d\t%.3f\n" % (puntoMenor,puntoMayor,anchoCable,bordeMenor))
              
              mat_datos_x.clear()

             #f.write(str(horaFecha)+"\t"+str(puntoMenor)+"\t"+ str(puntoMayor)+"\t"+str(puntoMenor*relacionPixel)+"\n")
             #f.write(str(puntoMenor)+"\t"+ str(puntoMayor)+"\t"+str(puntoMenor*relacionPixel)+"\n")
             #f.close
              
              puntoMenor=0
              puntoMayor=0
       #except:
        #      print("Imagen Mala para realizar el calculo")
              
#******************************************************************************


#************************************ Main ************************************

direccionCarpeta = 'C:/Users/milto/Milton/RSA/Proyectos/Proyecto Chanlud/Analisis/Coordinometros/Fotos/prueba/'

#nombreArchivo = input("Ingrese el nombre de la foto: ")
nombreArchivo = '2023-04-13 11_44_11.712927' 

imagen = direccionCarpeta + nombreArchivo + ".jpg"
#imagen = "Foto1.jpg"
              
ProcesarImagen(imagen,direccionCarpeta)

#******************************************************************************
