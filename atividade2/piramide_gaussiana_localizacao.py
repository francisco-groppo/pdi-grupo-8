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

    #transformação da imagem em float
    img = img.astype(float)
    num_rows, num_cols = img.shape

    #retorna a metade inteira da divisão por 2 das linhas e colunas
    half_num_rows = (num_rows+1)//2
    half_num_cols = (num_cols+1)//2

    #aplica a convolução para suavização da imagem
    img_smooth = convolve(img, filtro, mode='same')

    #cria um vetor de zeros, com a metade das linhas e colunas da matriz original
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

    #retorna a imagem contendo as diferenças
    return img_diff



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

        #pega o último valor e armazena na imagem
        img_down = piramide[-1]

        #o tamanho vai sendo dividido por 2
        new_tamanho = (tamanho+1)//2
        tamanho =  new_tamanho
        #chamamento da função que faz a suavização
        img_down = downsample(img_down)
        #adição da imagem reduzida e suavizada no vetor pirâmide
        piramide.append(img_down)

        #retornar a pirâmide invertida
    return piramide[::-1]

#função que retorna o menor valor existente entre a imagem e o objeto a ser localizado
def retorna_menor_valor(img, imgobject):
    imgA = []
    menor_valorA = []
    indiceA = []

    #aplicação da diferença quadrática entre a imagem e o objeto
    img_diferenca = diferenca_quadratica(img,imgobject)

    #as variáveis recebem os valores mínimos existentes na imagem diferente
    menor_valor, indice = encontra_minimo(img_diferenca)

    #adição dos valores encontrados em vetores
    imgA.append(img)
    menor_valorA.append(menor_valor)
    indiceA.append(indice)

    #retorna da imagem e dos valores mínimos
    return imgA, menor_valorA,indiceA

#função que retorna o índice da imagem onde foi localizado o objeto
def menor_valor(valor):
    pos = -1
    for i in range(len(menor_valorAB)-1,-1,-1):
        if menor_valorAB[i] == valor:
            pos = i

    return pos


if __name__ == "__main__":

    # img = cv2.imread('imagem_global.tiff')
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = img.astype(float)

    img = cv2.imread('flower_grayscale1.tiff')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype(float)

    # imgobject = cv2.imread('gato.tiff')
    # imgobject = cv2.cvtColor(imgobject, cv2.COLOR_BGR2GRAY)
    # imgobject = imgobject.astype(float)

    imgobject = cv2.imread('planta_pequena.tif')
    imgobject = cv2.cvtColor(imgobject, cv2.COLOR_BGR2GRAY)
    imgobject = imgobject.astype(float)


    #criação da pirâmide
    piramides = num_niveis(img)


    imgAB=[]
    menor_valorAB=[]
    indiceAB=[]


    #varre as imagens na pirâmide
    for pir in range (len(piramides)):

        imgA, menor_valorA,indice = retorna_menor_valor(piramides[pir], imgobject)
        imgAB.append(imgA)
        menor_valorAB.append(menor_valorA)
        indiceAB.append(indice)

        plt.imshow(piramides[pir], 'gray')
        plt.figure()


    #a variável pos recebe o menor valor do vetor de valores
    pos = menor_valor(np.min(menor_valorAB))


    #criação da função que gera um retângulo na imagem que contém o objeto
    half_num_rows_obj = imgobject.shape[0]//2
    half_num_cols_obj = imgobject.shape[1]//2
    centerA = indiceAB[pos][0][0]
    centerB = indiceAB[pos][0][1]

    #imagem retângulo recebe a cópia da pirâmide onde encontrou o objeto localizado
    img_rectangle = piramides[pos].copy()

    #criação do retângulo utilizando o cv2.rectangle do opencv
    pt1 = (centerB-half_num_cols_obj, centerA -half_num_rows_obj)
    pt2 = (centerB+half_num_cols_obj, centerA +half_num_rows_obj)
    cv2.rectangle(img_rectangle, pt1=pt1, pt2=pt2, color=255, thickness=3)

    #Plotagem do objeto localizado na pirâmide de imagens
    plt.title("imagem da pirâmide "+ str(pos) + ' / '+ str(len(piramides)-1) +', índice: '+ str(indiceAB[pos]) )
    plt.imshow(img_rectangle, 'gray')
    plt.figure()