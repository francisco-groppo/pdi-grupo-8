#!/usr/bin/env python
# coding: utf-8

# In[20]:


import numpy as np
import matplotlib.pyplot as plt
import cv2


def mirror_borda(original, borda):
    rows, columns = original.shape

    changed = np.zeros((rows+2*borda, columns+2*borda))

    # corners
    # top - left
    changed[0:borda, 0: borda] = np.flipud(
        np.fliplr(original[1:borda+1, 1: borda+1]))
    # bottom - left
    changed[rows + borda:,
            0: borda] = np.flipud(np.fliplr(original[rows-borda-1: -1,  1: borda+1]))
    # top - right
    changed[0: borda, columns +
            borda:] = np.flipud(np.fliplr(original[1:borda+1, columns-borda-1: -1]))
    # bottom - right
    changed[rows + borda:, columns + borda:] = np.flipud(
        np.fliplr(original[rows-borda-1: -1, columns-borda-1: -1]))

    # original
    changed[borda: rows+borda, borda: columns + borda] = original

    # left
    changed[borda: rows+borda,
            0: borda] = np.fliplr(original[0:rows, 1:borda+1])

    # right
    changed[borda: rows+borda, columns +
            borda:] = np.fliplr(original[0:rows, columns-borda-1: -1])

    # top
    changed[0: borda, borda: borda +
            columns] = np.flipud(original[1:borda+1, 0:columns])

    # bottom
    changed[rows+borda:, borda: borda +
            columns] = np.flipud(original[rows-borda-1:-1, 0:columns])

    return changed


def visualize(original, changed):
    plt.matshow(original)
    plt.matshow(changed)
    plt.show()


img = cv2.imread('cameraman.tiff')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# modificando o tamanho da imagem para uma matriz nxm
# img = cv2.resize(img, (3, 9))

borda = 2

if __name__ == "__main__":
    changed = mirror_borda(img, borda)
    print(changed)
    visualize(img, changed)

# In[ ]:
