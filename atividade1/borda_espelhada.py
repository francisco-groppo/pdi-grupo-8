#!/usr/bin/env python
# coding: utf-8

# In[20]:



import numpy as np
import matplotlib.pyplot as plt
import cv2


img = cv2.imread('cameraman.tiff')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# modificando o tamanho da imagem para uma matriz 3x3
img = cv2.resize(img, (10, 9))

original = np.array([
    [2, 3, 1, 4, 5],
    [1, 5, 3, 7, 4],
    [2, 9, 2, 0, 0],
    [8, 7, 2, 4, 3]
   
])

borda=2


rows, columns = original.shape

changed = np.zeros((rows+2*borda, columns+2*borda))


# corners 
#top -left
changed[0:borda, 0: borda] = np.flipud(np.fliplr(original[1:borda+1, 1: borda+1]))
#botton - left
changed[rows + borda:, 0: borda] = np.flipud(np.fliplr(original[rows-borda-1: -1,  1: borda+1]))
#top - right
changed[0: borda, columns +borda:] = np.flipud(np.fliplr(original[1:borda+1, columns-borda-1: -1]))
#botton - right
changed[rows + borda:, columns +borda:] = np.flipud(np.fliplr(original[rows-borda-1: -1, columns-borda-1: -1]))

# original
changed[borda: rows+borda, borda: columns + borda]= original

# left
changed[borda: rows+borda, 0: borda]  = np.fliplr(original[0:rows, 1:borda+1])

# right
changed[borda: rows+borda, rows+borda:] = np.fliplr(original[0:rows, columns-borda-1: -1])

# top
changed[0: borda, borda: borda + columns] = np.flipud(original[1:borda+1, 0:columns])

# bottom
changed[columns+borda:, borda : borda + columns] = np.flipud(original[rows-borda-1:-1, 0:columns])
print(original)
print(changed)


# In[ ]:




