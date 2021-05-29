#!/usr/bin/env python
# coding: utf-8

# In[20]:


import numpy as np
import matplotlib.pyplot as plt
import cv2
import time


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


def mirror_borda_2(img, borda):
    num_lin, num_col = img.shape

    half_r_size = num_lin//2        # O operador // retorna a parte inteira da divisão
    half_c_size = num_col//2
    borda = 4
    borda_lin = borda//2
    borda_col = borda//2

    # Cria imagem com zeros ao redor da borda
    img_padded = np.zeros((num_lin+borda, num_col+borda), dtype=img.dtype)
    for row in range(num_lin):
        for col in range(num_col):
            # top left
            img_padded[:borda_lin, :borda_col] = np.flip(
                img[borda_lin-1:borda_lin+1, borda_col-1:borda_col+1])
            # top right
            img_padded[:borda_lin, -(borda_col):] = np.flip(
                img[borda_lin-1:borda_lin+1, -borda_col-1:-borda_col+1])

            # botton left
            img_padded[-(borda_lin):, :borda_col] = np.flip(img[-borda_lin -
                                                            1:-(borda_lin-1), borda_col-1:(borda_col+1)])

            # botton right
            img_padded[-(borda_lin):, -(borda_col):] = np.flip(img[-borda_lin -
                                                                   1:-(borda_lin-1), -borda_col-1:-borda_col+1])

            # original
            img_padded[row+borda_lin, col+borda_col] = img[row, col]

    return img_padded


def visualize(original, changed):
    plt.matshow(original)
    plt.matshow(changed)
    plt.show()


img = cv2.imread('./atividade1/cameraman.tiff')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# modificando o tamanho da imagem para uma matriz nxm
# img = cv2.resize(img, (3, 9))

borda = 20

if __name__ == "__main__":
    start1 = time.time()
    changed = mirror_borda(img, borda)
    end1 = time.time()
    start2 = time.time()
    changed2 = mirror_borda_2(img, borda)
    end2 = time.time()
    print("Time elapsed with for loop: ", end2 - start2)
    print("Time elapsed with numpy: ", end1 - start1)
    visualize(img, changed)
    visualize(img, changed2)

# In[ ]:
