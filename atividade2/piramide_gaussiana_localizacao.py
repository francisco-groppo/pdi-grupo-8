# importe dos pacotes python
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve
import cv2

def downsample(img):
    '''Gera uma nova imagem com metade do tamanho da imagem de entrada. A imagem de
       entrada é suavizada utilizando um filtro gaussiano e amostrada a cada 2 pixels'''
    # Filtro gaussiano
    filtro = np.array([[1,  4,  6,  4, 1],
                       [4, 16, 24, 16, 4],
                       [6, 24, 36, 24, 6],
                       [4, 16, 24, 16, 4],
                       [1,  4,  6,  4, 1]])
    filtro = filtro/256.

    img = img.astype(float)
    num_rows, num_cols = img.shape
    half_num_rows = (num_rows+1)//2
    half_num_cols = (num_cols+1)//2

    img_smooth = convolve(img, filtro, mode='same')
    img_down = np.zeros([half_num_rows,half_num_cols])

    for row in range(0, half_num_rows):
        for col in range(half_num_cols):
            img_down[row, col] = img_smooth[2*row, 2*col]

    return img_down

def diferenca_quadratica(img, obj):
    '''Calcula a diferença quadrática entre as imagens img e obj. É assumido que img é maior do
       que obj. Portanto, a diferença é calculada para cada posição do centro da imagem obj ao
       longo de img. Note que a função é facilmente modificável para processar imagens coloridas.'''

    num_rows, num_cols = img.shape
    num_rows_obj, num_cols_obj = obj.shape

    half_num_rows_obj = num_rows_obj//2        # O operador // retorna a parte inteira da divisão
    half_num_cols_obj = num_cols_obj//2

    # Cria imagem com zeros ao redor da borda. Note que ao invés de adicionarmos 0, seria mais
    # preciso calcularmos a diferença quadrática somente entre pixels contidos na imagem.
    img_padded = np.pad(img, ((half_num_rows_obj,half_num_rows_obj),
                              (half_num_cols_obj,half_num_cols_obj)),
                        mode='constant')

    img_diff = np.zeros((num_rows, num_cols))
    for row in range(num_rows):
        for col in range(num_cols):
            # patch é a região de img de mesmo tamanho que obj e centrada em (row, col)
            patch = img_padded[row:row+num_rows_obj, col:col+num_cols_obj]
            # Utilizando numpy, o comando abaixo calcula a diferença entre cada valor
            # dos arrays 2D patch e obj
            diff_region = (patch - obj)**2
            img_diff[row, col] = np.sum(diff_region)

    return img_diff

def draw_rectangle(img_g, center, size):
    '''Desenha um quadrado em uma cópia do array img_g. center indica o centro do quadrado
       e size o tamanho.'''

    half_num_rows_obj = size[0]//2
    half_num_cols_obj = size[1]//2

    img_rectangle = img_g.copy()
    pt1 = (center[1]-half_num_cols_obj, center[0]-half_num_rows_obj)
    pt2 = (center[1]+half_num_cols_obj, center[0]+half_num_rows_obj)
    cv2.rectangle(img_rectangle, pt1=pt1, pt2=pt2, color=255, thickness=3)

    return img_rectangle

def encontra_minimo(img):
    '''Encontra posição do valor mínimo de img'''

    num_rows, num_cols = img.shape
    menor_valor = img[0,0]
    indice_menor_valor = (0, 0)
    for row in range(num_rows):
        for col in range(num_cols):
            valor = img[row,col]
            if valor<menor_valor:
                menor_valor = valor
                indice_menor_valor = (row, col)

    return menor_valor, indice_menor_valor


def num_niveis(img):
    num_rows, num_cols = img.shape

    #pega o menor tamanho entre colunas e linhas
    tamanho = num_rows if num_rows < num_cols else num_cols

    #vetor recebe a imagem original
    piramide = [img]

    #escalona a pirâmide até 3x3 no mínimo
    while tamanho > 2:

        img_down = piramide[-1]
        new_tamanho = (tamanho+1)//2
        tamanho =  new_tamanho
        img_down = downsample(img_down)
        piramide.append(img_down)

        #retornar a pirâmide invertida
    return piramide[::-1]

def retorna_menor_valor(img, imgobject):
    imgA = []
    menor_valorA = []
    indiceA = []

    img_diferenca = diferenca_quadratica(img,imgobject)

    menor_valor, indice = encontra_minimo(img_diferenca)

    print('Menor diferença: {}'.format(menor_valor))
    print('Posição: {}'.format(indice))
    imgA.append(img)
    menor_valorA.append(menor_valor)
    indiceA.append(indice)

    return imgA, menor_valorA,indiceA




if __name__ == "__main__":

    img = cv2.imread('imagem_global.tiff')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype(float)

    imgobject = cv2.imread('gato.tiff')
    imgobject = cv2.cvtColor(imgobject, cv2.COLOR_BGR2GRAY)
    imgobject = imgobject.astype(float)



    #esta parte debaixo seta o retângulo
    #img_square = draw_rectangle(img_g, indice, img_o.shape)
    #plt.imshow(img_square, 'gray')

    piramides = num_niveis(img)


    imgAB=[]
    menor_valorAB=[]
    indiceAB=[]
    vet = []
    num_rows_gato, num_cols_gato = imgobject.shape
    vet.append(num_rows_gato)
    vet.append(num_cols_gato)
    for pir in range (len(piramides)):
        # num_rows, num_cols = piramides[pir].shape
        #print(num_rows, num_cols)
        #plt.figure(figsize=[10,10])
        #plt.figure(figsize=[num_rows/40,num_cols/60])
        #plt.imshow(piramides[pir], 'gray')

        imgA, menor_valorA,indice = retorna_menor_valor(piramides[pir], imgobject)
        imgAB.append(imgA)
        menor_valorAB.append(menor_valorA)
        indiceAB.append(indice)


        # print(imagem_com_menor_valor)
        # plt.imshow(imagem_com_menor_valor, 'gray')
    valor = np.min(menor_valorAB)
    pos = -1
    for i in range(len(menor_valorAB)-1,-1,-1):
        if menor_valorAB[i] == valor:
            pos = i
    print(pos)

    #print('imgobject.shape: {}'.format(imgobject.shape))
    #print('piramides[pos]: {}'.format(piramides[pos].shape))
    #plt.imshow(piramides[pos], 'gray')


    print('Menor valorAB: {}'.format(menor_valorAB[pos]))
    print('Menor indice: {}'.format(indiceAB[pos]))


    half_num_rows_obj = imgobject.shape[0]//2
    half_num_cols_obj = imgobject.shape[1]//2
    centerA = indiceAB[pos][0][0]
    centerB = indiceAB[pos][0][1]

    img_rectangle = piramides[pos].copy()
    pt1 = (centerB-half_num_cols_obj, centerA -half_num_rows_obj)
    pt2 = (centerB+half_num_cols_obj, centerA +half_num_rows_obj)
    cv2.rectangle(img_rectangle, pt1=pt1, pt2=pt2, color=255, thickness=3)
    plt.title("imagem certa")
    plt.imshow(img_rectangle, 'gray')
    plt.figure()