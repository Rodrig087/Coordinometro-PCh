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
              #cv2.imwrite(direccionCarpeta+'filtroblur.jpg',gauss)
              canny = cv2.Canny(gauss, 30, 60)
                            
              lines = cv2.HoughLinesP(image=canny,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=180,maxLineGap=100)
              
              a,b,c = lines.shape
              
              for i in range(a):
                     cv2.line(gauss, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 255, 0), 3, cv2.LINE_AA)
                     mat_datos_x.append(lines[i][0][0])
              
              cv2.imwrite(direccionCarpeta+'lineasMarcadas.jpg',img)

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
        
def Procesar(Imagen, pathImagen, pathDatos):
    pathFoto = pathImagen + Imagen + '.jpg'
    mat_datos_x = []
    puntoMenor = 0

    global bordeMenorAnterior
    global desfaceAnterior
    global contadorErrores
    global contadorArchivosProcesados
    global contadorArchivosSinProcesar
    global contadorBordeUnico

    tiempoImagen = Imagen[0:19]
    tiempoImagen_dt = datetime.strptime(tiempoImagen, '%Y-%m-%d %H_%M_%S')
    tiempoImagen_str = tiempoImagen_dt.strftime('%Y-%m-%dT%H:%M:%S')

    try:
        img = cv2.imread(pathFoto)
        height, width = img.shape[:2]
        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gauss = cv2.medianBlur(gris, 13)

        # Define los pares de umbrales para probar con Canny
        canny_thresholds = [(100,120)]
        lines_found = False

        for thresholds in canny_thresholds:
            if not lines_found:
                canny = cv2.Canny(gauss, thresholds[0], thresholds[1])
                lines = cv2.HoughLinesP(image=canny, rho=1, theta=np.pi / 180, threshold=100, lines=np.array([]),
                                        minLineLength=180, maxLineGap=100)
                if lines is not None:
                    lines_found = True
                    a, b, c = lines.shape
                    for i in range(a):
                        cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 255, 0), 3,
                                 cv2.LINE_AA)
                        mat_datos_x.append(lines[i][0][0])
                    # Guardar la imagen después de procesar todas las líneas
                    #cv2.imwrite(pathDatos + Imagen + '.jpg', img)
                    cv2.imwrite(pathDatos + 'verticales.jpg', img)
                    puntoMayor = max(mat_datos_x)
                    puntoMenor = min(mat_datos_x)
                    
                    break  # Salir del bucle si se han encontrado líneas

        if not lines_found:
            # Si no se encontraron líneas con ninguno de los umbrales, proceder con la lógica de error
            puntoMayor = 'null'
            puntoMenor = 'null'
                        

    except Exception as e:
        print(f"Error al procesar la imagen {Imagen}: {e}")
        puntoMayor = 'null'
        puntoMenor = 'null'
                
    #print(str(tiempoImagen_str) + ' ' + str(puntoMenor) + ' ' + str(puntoMayor))
    resultado = "{} {} {}".format(tiempoImagen_str, puntoMenor, puntoMayor)
    print(resultado)
    
    
def DeteccionVertical(Imagen, pathImagen, pathDatos):
    pathFoto = pathImagen + Imagen + '.jpg'
    mat_datos_x = []
    
    global contadorErrores
    global contadorArchivosProcesados
    global contadorArchivosSinProcesar

    tiempoImagen = Imagen[0:19]
    tiempoImagen_dt = datetime.strptime(tiempoImagen, '%Y-%m-%d %H_%M_%S')
    tiempoImagen_str = tiempoImagen_dt.strftime('%Y-%m-%dT%H:%M:%S')

    try:
        img = cv2.imread(pathFoto)
        if img is None:
            raise ValueError("No se pudo cargar la imagen.")

        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gauss = cv2.medianBlur(gris, 13)
        
        # Aplicar el filtro Sobel en el eje x (bordes verticales)
        sobelx = cv2.Sobel(gauss, cv2.CV_64F, 1, 0, ksize=5)
        
        # Umbralizar la imagen de Sobel para prepararla para la detección de líneas
        _, sobelx_thresh = cv2.threshold(cv2.convertScaleAbs(sobelx), 50, 255, cv2.THRESH_BINARY)
        
        # Uso de HoughLinesP para detectar líneas verticales
        lines = cv2.HoughLinesP(sobelx_thresh, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=20)
        
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    # Asegurarse de que las líneas son verticales
                    if x1 == x2:
                        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                        mat_datos_x.append(x1)
            
            # Guardar la imagen con líneas verticales marcadas
            #cv2.imwrite(pathImagen + 'tmp/' + Imagen + '.jpg', img)
            cv2.imwrite(pathDatos + 'verticales.jpg', img)
            puntoMayor = max(mat_datos_x)
            puntoMenor = min(mat_datos_x)
            
        else:
            raise ValueError("No se encontraron líneas verticales en la imagen.")

    except Exception as e:
        print(f"Error al procesar la imagen {Imagen}: {e}")
        puntoMayor = 'null'
        puntoMenor = 'null'
       
    print(str(tiempoImagen_str) + ' ' + str(puntoMenor) + ' ' + str(puntoMayor))
    
              
#******************************************************************************


#************************************ Main ************************************

#direccionCarpeta = 'C:/Users/milto/Milton/RSA/Proyectos/Proyecto Chanlud/Analisis/Coordinometros/Fotos/prueba/'
#direccionCarpeta = 'C:/Users/RSA-Milton/Desktop/Coordinometros/Fotos/IZQ/IZQ-N2-X/'

#******************************************************************************
eje = 'IZQ'
idEstacion = 'IZQ-N2-X'
anio = '2022'
#******************************************************************************  
directorioFotos = 'C:/Users/RSA-Milton/Desktop/Coordinometros/Fotos/' + eje + '/' + idEstacion + '/' + anio + '/'
directorioDatos = 'C:/Users/RSA-Milton/Desktop/Coordinometros/Fotos/' + eje + '/' + idEstacion + '/' 
#******************************************************************************

#nombreArchivo = input("Ingrese el nombre de la foto: ")
nombreArchivo = '2022-01-01 14_00_11.251146' 

imagen = directorioFotos + nombreArchivo + ".jpg"
#imagen = "Foto1.jpg"
              
#ProcesarImagen(imagen,directorioDatos)
Procesar(nombreArchivo, directorioFotos,directorioDatos)
#eteccionVertical(nombreArchivo, directorioFotos,directorioDatos)

#******************************************************************************
