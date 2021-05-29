#!/usr/bin/env python
# coding: utf-8

# In[24]:


#!/usr/bin/env python
# coding: utf-8

# In[112]:


import numpy as np
import matplotlib.pyplot as plt
import cv2


def nearest_neighbor_fill(original, borda):
    rows, columns = original.shape

    changed = np.zeros((rows+2*borda, columns+2*borda))

    # corners
    # top - left
    changed[0:borda + 1, 0: borda + 1] = original[0, 0]
    # bottom - left
    changed[rows + borda - 1:, 0: borda + 1] = original[rows-1, 0]
    # top - right
    changed[0:borda + 1, columns + borda - 1:] = original[0, columns-1]
    # bottom - right
    changed[rows + borda - 1:, columns +
            borda - 1:] = original[rows-1, columns-1]

    # original
    changed[borda: rows + borda, borda: columns + borda] = original

    # left
    changed[borda + 1: rows + borda - 1,
            0: borda] = np.array([original[1:rows-1, 0]]).T

    # right
    changed[borda + 1: rows + borda - 1, columns +
            borda:] = np.array([original[1:rows-1, -1]]).T

    # top
    changed[0: borda, borda + 1: columns +
            borda - 1] = original[0, 1:columns-1]

    # bottom
    changed[rows + borda:, borda + 1: columns +
            borda - 1] = original[-1, 1:columns-1]

    return changed


def visualize(original, changed):
    plt.matshow(original)
    plt.matshow(changed)
    plt.show()


img = cv2.imread('cameraman.tiff')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# modificando o tamanho da imagem para uma matriz nxm
# img = cv2.resize(img, (48, 48))

original = img

borda = 2

if __name__ == "__main__":
    changed = nearest_neighbor_fill(img, borda)
    print(changed)
    visualize(img, changed)

# In[ ]:


# In[ ]:
