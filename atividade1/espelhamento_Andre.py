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

# img = cv2.resize(img,(101,100))



num_lin, num_col = img.shape

#Define os valores de bordas para nova imagem
borda = 4
#Define os valores de bordas das linha (esquerda e direita) para nova imagem
borda_lin = borda//2
#Define os valores de bordas das coluna (cima e baixo) para nova imagem
borda_col = borda//2



# Cria a nova imagem de zeros
img_padded = np.zeros((num_lin+borda, num_col+borda), dtype=img.dtype)
for row in range(num_lin):
    for col in range(num_col):               
            #top left, define os valores da borda de cima a esquerda da nova imagem com base
            # da diagonal primeira (esquerda para direita, cima para baixo) de forma espelhada
            img_padded[:borda_lin, :borda_col] = np.flip(img[1:borda_lin+1, 1:borda_col+1])
            
            #top right,define os valores da borda de cima a direita da nova imagem com base
            # da diagonal segundaria (direita para esquerda , cima para baixo) de forma espelhada          
            img_padded[:borda_lin,-(borda_col):] = np.flip(img[1:borda_lin+1, -borda_col-1:-1])
            
            #botton left, define os valores da borda de baixo a esquerda da nova imagem com base
            # da diagonal segundaria (esquerda para direita, baixo para cima) de forma espelhada
            img_padded[-(borda_lin):, :borda_col] =  np.flip(img[-borda_lin-1:-1,  1:borda_col+1])
            
            #botton right, define os valores da borda de baixo a direita da nova imagem com base
            # da diagonal primeira (direita para esquerda , baixo para cima) de forma espelhada
            img_padded[ -(borda_lin):, -(borda_col):]= np.flip(img[-borda_lin-1:-1, -borda_col-1:-1])
            
            #original, coloca a imagem "img" de forma centralizada na nova imagem
            img_padded[row+borda_lin, col+borda_col] = img[row, col]
            
plt.imshow(img_padded, 'gray')
plt.figure()



num_lin1,num_col1=img_padded.shape
img_padded1 = img_padded.copy()

for row in range(num_lin1):
    for col in range(num_col1):
        # right, os valores 0 restantes a borda direita da nova imagem é feito o espelhamento referente aquela região 
        img_padded1[borda_lin:-borda_lin, borda_col+num_col:] = np.fliplr(img[:,-borda_col-1:-1])                                                            
        #top, os valores 0 restantes a borda em cima da nova imagem é feito o espelhamento referente aquela região     
        img_padded1[:borda_lin, borda_col:-(borda_col)] = np.flipud(img[1:borda_lin+1,:])
        #left, os valores 0 restantes a borda esquerda da nova imagem é feito o espelhamento referente aquela região     
        img_padded1[(borda_lin):-borda_lin, :borda_col] = np.fliplr(img[:,1:borda_col+1])
        #botton, os valores 0 restantes a borda em baixo da nova imagem é feito o espelhamento referente aquela região     
        img_padded1[-(borda_lin):,borda_col:-(borda_col)] = np.flipud(img[-(borda_lin+1):-1,:])
# resultado final da técnica de preenchimento de borda       
print(img_padded1)  
plt.imshow(img_padded1, 'gray')
plt.figure()  
       

