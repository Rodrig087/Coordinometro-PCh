import numpy as np
import cv2
from datetime import date
from datetime import datetime
import os
import time


# ////////////////////////////////// Metodos //////////////////////////////////

def ProcesarImagen(pathImagen, pathDatos):
       
       mat_datos_x=[]
       puntoMenor=0
       
       global bordeMenorAnterior
       global desfaceAnterior
       
       global contadorErrores
       global contadorArchivosProcesados
       global contadorArchivosSinProcesar
       
       try:
       ####################-Procesamiento de Imagen-##########################
       #######################################################################
       
              tiempoImagen = pathImagen[54:73]  
              tiempoImagen_dt = datetime.strptime(tiempoImagen, '%Y-%m-%d %H_%M_%S')
              tiempoImagen_str = str(tiempoImagen_dt)
       
              img = cv2.imread(pathImagen)
              height, width = img.shape[:2]
                
              gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
              gauss = cv2.medianBlur(gris,13)
              #gauss = cv2.GaussianBlur(gris, (3,3), 0)
              #cv2.imwrite(pathDatos[0:43]+'filtroblur.jpg',gauss)
              
              canny = cv2.Canny(gauss, 100, 150)
              #canny = cv2.Canny(gauss, 10, 50)
              #canny = cv2.Canny(gauss, 5, 10)
                            
              lines = cv2.HoughLinesP(image=canny,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=180,maxLineGap=100)
                     
              a,b,c = lines.shape

              f = open(pathDatos,"a")

              for i in range(a):
                     cv2.line(gauss, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
                     #print(lines[i][0][0], lines[i][0][1], lines[i][0][2], lines[i][0][3])
                     mat_datos_x.append(lines[i][0][0])
                     #cv2.imwrite(direccionCarpeta+'lineasMarcadas.jpg',gauss)
                     #cv2.imwrite(pathDatos[0:43]+'lineasMarcadas.jpg',gauss)

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
              
       except:
           
              print("No se pudo realizar el calculo")
              contadorArchivosSinProcesar = contadorArchivosSinProcesar + 1
              
 # /////////////////////////////////////////////////////////////////////////////



# ///////////////////////////////// Principal /////////////////////////////////

if __name__ == '__main__':
    
    #******************************************************************************
    #Obtiene el nombre de todos los archivos:
    #Lista los archivos del directorio a subir
    nombreEje = "EJE2"
    nombreDispositivo = "N1_X"
    nombreArchivoMediciones = nombreEje + nombreDispositivo + ".txt"
    rutaArchivos = "C:/Users/milto/Desktop/Coordinometros/"+nombreEje+"/Fotos/" + nombreDispositivo + "/"
    print(rutaArchivos)
    listaArchivos = os.listdir(rutaArchivos)
    listaArchivosOrdenada = sorted(listaArchivos) 
    listaArchivosOrdenada = listaArchivosOrdenada[0:(len(listaArchivosOrdenada)-3)]
    #print(listaArchivosOrdenada)    
    #******************************************************************************
    
    #******************************************************************************
    #Lee o crea el archivo de mediciones:
    pathArchivoMediciones = rutaArchivos[0:43]+nombreArchivoMediciones        
    #archivoMediciones = open(pathArchivoMediciones,"a")
    pathDatos = pathArchivoMediciones
    #******************************************************************************
    
    bordeMenorAnterior = 0
    desfaceAnterior = 0
    contadorArchivosProcesados = 0
    contadorErrores = 0
    contadorArchivosSinProcesar = 0
    
    for nombreImagen in listaArchivosOrdenada:
        
        pathImagen = rutaArchivos + nombreImagen   
        ProcesarImagen(pathImagen, pathDatos)
        
    #archivoMediciones.close()
    
    print("Numero total de archivos: %d" %(len(listaArchivosOrdenada))) 
    print("Numero de archivos procesados: %d" %contadorArchivosProcesados)
    print("Numero de archivos sin procesar: %d" %contadorArchivosSinProcesar)
    print("Numero de archivos con errores: %d" %contadorErrores)

# /////////////////////////////////////////////////////////////////////////////            
