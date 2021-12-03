# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 10:36:36 2021

@author: ivan.palacios
"""

import cv2
 
# Cargamos la imagen del disco duro
imagen = cv2.imread("logo.png")
 
cv2.imshow("RPi", imagen)
cv2.waitKey(0)