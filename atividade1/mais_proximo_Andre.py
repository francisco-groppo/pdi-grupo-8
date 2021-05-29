# -*- coding: utf-8 -*-
"""
Created on Sun May 23 18:01:08 2021

@author: andre
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2


img = cv2.imread('cameraman.tiff')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.figure(figsize=[7,7])
plt.imshow(img, 'gray')
plt.figure()

img = cv2.resize(img,(200,100))
num_lin, num_col = img.shape



borda = 4
borda_lin = borda//2
borda_col = borda//2



# Cria imagem com zeros ao redor da borda
img_padded = np.zeros((num_lin+borda, num_col+borda), dtype=img.dtype)
for row in range(num_lin):
    for col in range(num_col):   
            img_padded[row+borda_lin, col+borda_col] = img[row, col]
            #top left
            img_padded[:borda_lin+1, :borda_col+1] = img[:-(num_lin-1), :-(num_col-1)]
            #top right            
            img_padded[:borda_lin+1,-(borda_col+1):] = img[:-(num_lin-1),num_col-1:]
            
            #botton left
            img_padded[-(borda_lin+1):, :borda_col+1] = img[(num_lin-1):,:-(num_col-1)]
            
            #botton right
            img_padded[-(borda_lin+1):, -(borda_col+1):]= img[(num_lin-1):,num_col-1:]
            
plt.imshow(img_padded, 'gray')
plt.figure()
print(img)
print("\n")
print(img_padded)
print("\n")
#.........................................................

num_lin,num_col=img_padded.shape
img_padded1 = img_padded.copy()

for row in range(num_lin):
    for col in range(num_col):
        # right
        img_padded1[(borda_lin+1):-borda_lin-1, -(borda_col):] = img[1:-1,-1:]
        #top        
        img_padded1[:borda_lin, borda_col+1:-(borda_col+1)] = img[:1,1:-1]
        #left
        img_padded1[(borda_lin+1):-borda_lin-1, :borda_col] = img[1:-1,:1]
        #botton
        img_padded1[-(borda_lin):,borda_col+1:-(borda_col+1)] = img[-1:,1:-1]
        
print(img_padded1)  
plt.imshow(img_padded1, 'gray')
plt.figure()      

plt.subplot(1,3,1)
plt.imshow(img, 'gray')
plt.subplot(1,3,2)
plt.imshow(img_padded, 'gray')
plt.subplot(1,3,3)
plt.imshow(img_padded1, 'gray')
plt.figure() 

