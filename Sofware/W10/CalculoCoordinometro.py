import numpy as np
import cv2
from datetime import date
from datetime import datetime
import os
import time


# ////////////////////////////////// Metodos //////////////////////////////////

def ProcesarImagen(Imagen, pathImagen, pathDatos):
       
       mat_datos_x=[]
       puntoMenor=0
       
       global bordeMenorAnterior
       global desfaceAnterior
       
       global contadorErrores
       global contadorArchivosProcesados
       global contadorArchivosSinProcesar
       
       '''
       tiempoImagen = Imagen[0:19]  
       tiempoImagen_dt = datetime.strptime(tiempoImagen, '%Y-%m-%d %H_%M_%S')
       tiempoImagen_formateado = tiempoImagen_dt.strftime('%Y-%m-%dT%H:%M:%S')
       print(tiempoImagen_formateado)
       #img = cv2.imread(pathImagen+Imagen)
       '''
       try:
       ####################-Procesamiento de Imagen-##########################
       #######################################################################
       
              tiempoImagen = Imagen[0:19]  
              tiempoImagen_dt = datetime.strptime(tiempoImagen, '%Y-%m-%d %H_%M_%S')
              tiempoImagen_str = tiempoImagen_dt.strftime('%Y-%m-%dT%H:%M:%S')
              print(tiempoImagen_str)
       
              pathFoto =  pathImagen+Imagen      
       
              img = cv2.imread(pathFoto)
              height, width = img.shape[:2]
                
              gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
              gauss = cv2.medianBlur(gris,13)
                            
              canny = cv2.Canny(gauss, 20, 60)
                                         
              lines = cv2.HoughLinesP(image=canny,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=180,maxLineGap=100)
                     
              a,b,c = lines.shape

              #f = open(pathDatos,"a")

              for i in range(a):
                  '''   
                  cv2.line(gauss, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
                  #print(lines[i][0][0], lines[i][0][1], lines[i][0][2], lines[i][0][3])
                  mat_datos_x.append(lines[i][0][0])
                  #cv2.imwrite(direccionCarpeta+'lineasMarcadas.jpg',gauss)
                  #cv2.imwrite(pathDatos[0:43]+'lineasMarcadas.jpg',gauss)
                  '''
                  cv2.line(gauss, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 255, 0), 3, cv2.LINE_AA)
                  mat_datos_x.append(lines[i][0][0])
                  cv2.imwrite(pathDatos+'lineasMarcadas.jpg',gauss)
              
              puntoMayor = max(mat_datos_x)
              puntoMenor = min(mat_datos_x)
              
              
              
              print(puntoMayor + puntoMenor)
              
              '''
              puntoMayor = max(mat_datos_x)
              puntoMenor = min(mat_datos_x)
              #anchoCable=215
              anchoCable = puntoMayor - puntoMenor
              anchoCable = 207
              relacionPixel = 2/anchoCable
              bordeMenor = puntoMenor*relacionPixel       
              bordeMenor_str = str("{0:.3f}".format(bordeMenor))
                            
              #if (anchoCable<202 or anchoCable>248):
              if (anchoCable<200 or anchoCable>300):
                  bordeMenor_str = "null"
                  desface = desfaceAnterior
                  desface_str = str("{0:.3f}".format(desface))
                  contadorErrores = contadorErrores + 1
              else:
                  desface = bordeMenor - bordeMenorAnterior
                  desfaceAnterior = desface
                  bordeMenorAnterior = bordeMenor
                  desface_str = str("{0:.3f}".format(desface))
                  contadorArchivosProcesados = contadorArchivosProcesados + 1
              
              print(tiempoImagen_str + "\t%d\t%d\t%d\t"%(puntoMenor,puntoMayor,anchoCable) + bordeMenor_str + "\t" + desface_str + "\n")
              
              mat_datos_x.clear()

              #f.write(tiempoImagen_str+"\t"+str(puntoMenor)+"\t"+ str(puntoMayor)+"\t"+str(anchoCable)+"\t"+bordeMenor_str+"\t"+desface_str+"\n")
              f.write(tiempoImagen_str + "\t" + desface_str + "\n")
              f.close
              
              puntoMenor=0
              puntoMayor=0
              
              '''
              
       except:
           
              print("No se pudo realizar el calculo")
              contadorArchivosSinProcesar = contadorArchivosSinProcesar + 1
       
              
 # /////////////////////////////////////////////////////////////////////////////



def Procesar(Imagen, pathImagen, pathDatos):
       
       mat_datos_x=[]
       puntoMenor=0
       
       global bordeMenorAnterior
       global desfaceAnterior
       global contadorErrores
       global contadorArchivosProcesados
       global contadorArchivosSinProcesar
       
             
       tiempoImagen = Imagen[0:19]  
       tiempoImagen_dt = datetime.strptime(tiempoImagen, '%Y-%m-%d %H_%M_%S')
       tiempoImagen_str = tiempoImagen_dt.strftime('%Y-%m-%dT%H:%M:%S')
       #print(tiempoImagen_str)
        
       img = cv2.imread(pathImagen+Imagen)
       height, width = img.shape[:2]
       
                             
       gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       gauss = cv2.medianBlur(gris,13)
       cv2.imwrite(pathDatos+'filtroblur.jpg',gauss)
       canny = cv2.Canny(gauss, 10, 30)
       
       print('llego')
                        
       lines = cv2.HoughLinesP(image=canny,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=180,maxLineGap=100)
       a,b,c = lines.shape

        #f = open(pathDatos,"a")

       for i in range(a):
           cv2.line(gauss, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 255, 0), 3, cv2.LINE_AA)
           mat_datos_x.append(lines[i][0][0])
           cv2.imwrite(pathDatos+'lineasMarcadas.jpg',gauss)
        
       puntoMayor = max(mat_datos_x)
       puntoMenor = min(mat_datos_x)
        
       print(str(tiempoImagen_str) + ' ' + str(puntoMayor) + ' ' + str(puntoMenor))




# ///////////////////////////////// Principal /////////////////////////////////

if __name__ == '__main__':
    
    #******************************************************************************
    # Directorio donde estan las fotos a procesar y directorio donde se guardara el archivo de respuesta
    directorioFotos= 'C:/Users/milto/Milton/RSA/Proyectos/Proyecto Chanlud/Analisis/Coordinometros/Fotos/IZQ/IZQ-N2-X/2023/'
    directorioDatos = 'C:/Users/milto/Milton/RSA/Proyectos/Proyecto Chanlud/Analisis/Coordinometros/Fotos/IZQ/IZQ-N2-X/'
    #******************************************************************************
    #Obtiene el nombre de todas las fotos del directorio:
    listaArchivos = os.listdir(directorioFotos)
    listaArchivosOrdenada = sorted(listaArchivos) 
    listaArchivosOrdenada = listaArchivosOrdenada[0:(len(listaArchivosOrdenada))]
    #print(listaArchivosOrdenada)
    #******************************************************************************
    # Procesa las fotos una por una    
    bordeMenorAnterior = 0
    desfaceAnterior = 0
    contadorArchivosProcesados = 0
    contadorErrores = 0
    contadorArchivosSinProcesar = 0
    
    for foto in listaArchivosOrdenada:
        Procesar(foto, directorioFotos, directorioDatos)
        
    #archivoMediciones.close()
        
    print("Numero total de archivos: %d" %(len(listaArchivosOrdenada))) 
    print("Numero de archivos procesados: %d" %contadorArchivosProcesados)
    print("Numero de archivos sin procesar: %d" %contadorArchivosSinProcesar)
    print("Numero de archivos con errores: %d" %contadorErrores)
    
    print(listaArchivosOrdenada[0][0:19])
    
    #******************************************************************************

# /////////////////////////////////////////////////////////////////////////////            
