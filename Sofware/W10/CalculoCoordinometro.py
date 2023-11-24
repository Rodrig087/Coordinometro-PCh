import numpy as np
import cv2
from datetime import date
from datetime import datetime
import os
import time


# ////////////////////////////////// Metodos //////////////////////////////////

def ProcesarImagen(Imagen, idCoor, anio, pathImagen, pathDatos):
    pathFoto = pathImagen + Imagen
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
        canny_thresholds = [(30, 90), (30, 60), (20, 60), (20, 40), (10, 30), (10, 20)]
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
                    cv2.imwrite(pathImagen + 'tmp/' + Imagen + '.jpg', img)
                    puntoMayor = max(mat_datos_x)
                    puntoMenor = min(mat_datos_x)
                    grosorPx = puntoMayor - puntoMenor
                    contadorArchivosProcesados += 1
                    if (puntoMayor<(puntoMenor+50)):
                        contadorBordeUnico +=1
                        # Escribir los archivos con borde unico en un archivo de texto
                        archivo_uniborde = os.path.join(pathDatos, f"{idCoor}_uni-borde.txt")
                        with open(archivo_uniborde, 'a') as archivo:
                            archivo.write(foto + '\n')
                        # Obtien la media de un borde difuso
                        if (puntoMayor<(puntoMenor+25)):
                            grosorPx = 'null'
                            mediaBordeDifuso = (puntoMayor-puntoMenor)/2
                            puntoMenor = puntoMenor+int(mediaBordeDifuso)
                            puntoMayor = puntoMenor
                    break  # Salir del bucle si se han encontrado líneas

        if not lines_found:
            # Si no se encontraron líneas con ninguno de los umbrales, proceder con la lógica de error
            puntoMayor = 'null'
            puntoMenor = 'null'
            grosorPx = 'null'
            contadorErrores += 1
            # Escribir los archivos con sin bordes en un archivo de texto
            archivo_sinborde = os.path.join(pathDatos, f"{idCoor}_sin-borde.txt")
            with open(archivo_sinborde, 'a') as archivo:
                archivo.write(foto + '\n')
                
        resultado = "{} {} {} {}".format(tiempoImagen_str, puntoMenor, puntoMayor, grosorPx)
        print(resultado)
        # Escribir el resultado en un archivo de texto
        archivo_resultado = os.path.join(pathDatos, f"{idCoor}_{anio}.txt")
        with open(archivo_resultado, 'a') as archivo:
            archivo.write(resultado + '\n')

    except Exception as e:
        print(f"Error al procesar la imagen {Imagen}: {e}")
        puntoMayor = 'null'
        puntoMenor = 'null'
        grosorPx = 'null'
        contadorArchivosSinProcesar += 1
        # Escribir los archivos con sin procesar en un archivo de texto
        archivo_sinprocesar = os.path.join(pathDatos, f"{idCoor}_sin-procesar.txt")
        with open(archivo_sinprocesar, 'a') as archivo:
            archivo.write(foto + '\n')

    

def DeteccionVertical(Imagen, pathImagen, pathDatos):
    pathFoto = pathImagen + Imagen
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
            cv2.imwrite(pathImagen + 'tmp/' + Imagen + '.jpg', img)
            puntoMayor = max(mat_datos_x)
            puntoMenor = min(mat_datos_x)
            contadorArchivosProcesados += 1
        else:
            raise ValueError("No se encontraron líneas verticales en la imagen.")

    except Exception as e:
        print(f"Error al procesar la imagen {Imagen}: {e}")
        puntoMayor = 'null'
        puntoMenor = 'null'
        contadorArchivosSinProcesar += 1
        contadorErrores += 1

    print(str(tiempoImagen_str) + ' ' + str(puntoMenor) + ' ' + str(puntoMayor))

#//////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////// Principal /////////////////////////////////

if __name__ == '__main__':
    
    #******************************************************************************
    eje = 'IZQ'
    idEstacion = 'IZQ-N3-Y'
    anio = '2023'
    #******************************************************************************  
    directorioFotos = 'C:/Users/RSA-Milton/Desktop/Coordinometros/Fotos/' + eje + '/' + idEstacion + '/' + anio + '/'
    directorioDatos = 'C:/Users/RSA-Milton/Desktop/Coordinometros/Fotos/' + eje + '/' + idEstacion + '/' 
    #******************************************************************************
    #Obtiene el nombre de todas las fotos del directorio:
    listaArchivos = os.listdir(directorioFotos)
    listaArchivosOrdenada = sorted(listaArchivos) 
    listaArchivosOrdenada = listaArchivosOrdenada[0:(len(listaArchivosOrdenada)-1)]
    #print(listaArchivosOrdenada)
    #******************************************************************************
    # Procesa las fotos una por una    
    bordeMenorAnterior = 0
    desfaceAnterior = 0
    contadorArchivosProcesados = 0
    contadorErrores = 0
    contadorArchivosSinProcesar = 0
    contadorBordeUnico = 0
    
    for foto in listaArchivosOrdenada:
        ProcesarImagen(foto, idEstacion, anio, directorioFotos, directorioDatos)
        
    #archivoMediciones.close()
        
    print("Numero total de fotos: %d" %(len(listaArchivosOrdenada))) 
    print("Numero de fotos procesados: %d" %contadorArchivosProcesados)
    print("Numero de fotos con borde unico: %d" %contadorBordeUnico)
    print("Numero de fotos sin borde: %d" %contadorArchivosSinProcesar)
    print("Numero de fotos con errores: %d" %contadorErrores)
    
    
    #******************************************************************************

# /////////////////////////////////////////////////////////////////////////////            
