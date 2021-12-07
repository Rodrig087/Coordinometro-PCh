# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 10:36:36 2021

@author: ivan.palacios
"""

import cv2

direccionCarpeta = "D:/Proyecto Chanlud/Analisis/Coordinometros/fotos/"
nombreImagen = input("Ingrese el nombre de la imagen: ")
#nombreImagen = "logo" 
nombreArchivo = direccionCarpeta + nombreImagen + ".jpg"
 
# Cargamos la imagen del disco duro
imagen = cv2.imread(nombreArchivo)
 
cv2.imshow("Imagen", imagen)
cv2.waitKey(0)