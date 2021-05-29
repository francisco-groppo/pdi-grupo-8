# -*- coding: utf-8 -*-
"""
Created on Tue May 25 11:26:18 2021

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

img = cv2.resize(img,(300,300))


# img = np.array([
#     [2, 3, 1, 4],
#     [1, 5, 3, 7],
#     [2, 9, 2, 0],
#     [8, 7, 2, 4]
   
# ])

num_lin, num_col = img.shape


borda =8
borda_lin = borda//2
borda_col = borda//2



# Cria imagem com zeros ao redor da borda
img_padded = np.zeros((num_lin+borda, num_col+borda), dtype=img.dtype)
for row in range(num_lin):
    for col in range(num_col):               
            #top left
            img_padded[:borda_lin, :borda_col] = np.flip(img[1:borda_lin+1, 1:borda_col+1])
            #top right            
            img_padded[:borda_lin,-(borda_col):] = np.flip(img[1:borda_lin+1, -borda_col-1:-1])
            
            #botton left
            img_padded[-(borda_lin):, :borda_col] =  np.flip(img[-borda_lin-1:-1,  1:borda_col+1])
            
            #botton right
            img_padded[ -(borda_lin):, -(borda_col):]= np.flip(img[-borda_lin-1:-1, -borda_col-1:-1])
            
            #original
            img_padded[row+borda_lin, col+borda_col] = img[row, col]
            
plt.imshow(img_padded, 'gray')
plt.figure()
print(img)
print("\n")
print(img_padded)
print("\n")
#.........................................................

num_lin1,num_col1=img_padded.shape
img_padded1 = img_padded.copy()

for row in range(num_lin1):
    for col in range(num_col1):
        # right
        img_padded1[borda_lin:-borda_lin, borda_col+num_col:] = np.fliplr(img[:,-borda_col-1:-1])                                                            
        #top        
        img_padded1[:borda_lin, borda_col:-(borda_col)] = np.flipud(img[1:borda_lin+1,:])
        #left
        img_padded1[(borda_lin):-borda_lin, :borda_col] = np.fliplr(img[:,1:borda_col+1])
        #botton
        img_padded1[-(borda_lin):,borda_col:-(borda_col)] = np.flipud(img[-(borda_lin+1):-1,:])
        
print(img_padded1)  
plt.imshow(img_padded1, 'gray')
plt.figure()      

       

