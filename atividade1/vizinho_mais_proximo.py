#!/usr/bin/env python
# coding: utf-8

# In[24]:


#!/usr/bin/env python
# coding: utf-8

# In[112]:


import numpy as np
import matplotlib.pyplot as plt
import cv2


img = cv2.imread('cameraman.tiff')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# modificando o tamanho da imagem para uma matriz 3x3
img = cv2.resize(img, (10, 9))



########### Francisco ##############

print('----------------')

original = img

rows, columns = original.shape
#print(rows)
#print(columns)

changed = np.zeros((rows+4, columns+4))
#print(original[rows-1, 0])

# corners
changed[0:3, 0: 3] = original[0, 0]
changed[rows+1:, 0: 3] = original[rows-1, 0]
changed[0:3, columns+1:] = original[0, columns-1]
changed[rows +1:, columns+1:] = original[rows-1, columns-1]

# original
changed[2: rows+2, 2: columns +2] = original

# left
changed[3: rows+1, 0: 2] = np.array([original[1:rows-1, 0]]).T

# right
changed[3: rows+1, columns + 2:] = np.array([original[1:rows-1, -1]]).T

# top
changed[0: 2, 3: columns +1] = original[0, 1:columns-1]


# bottom
changed[rows +2:, 3: columns +1] = original[-1, 1:columns-1]

#plt.matshow(original)
#plt.matshow(changed)
#plt.show()

print(f'Original:\n {img}\n')


print(f'Com pad nos cantos:\n {changed.astype(int)}\n')

#print(changed.astype(int))

# In[ ]:


# In[ ]:




