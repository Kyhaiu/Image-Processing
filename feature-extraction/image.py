import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import functools
import copy
from scipy import ndimage

neighbors ={
    "n_0": [ 0, -1],
    "n_1": [-1, -1],
    "n_2": [-1,  0],
    "n_3": [-1,  1],
    "n_4": [ 0,  1],
    "n_5": [ 1,  1],
    "n_6": [ 1,  0],
    "n_7": [ 1, -1]
}

inverse_neighbors ={
    "[0, -1]" : 0,
    "[-1, -1]": 1,
    "[-1, 0]" : 2,
    "[-1, 1]" : 3,
    "[0, 1]"  : 4,
    "[1, 1]"  : 5,
    "[1, 0]"  : 6,
    "[1, -1]" : 7
}

class image:
    def __init__(self, _filename):
        """
            Constutor da classe image
            -------------------------

            Parametros:
                _filename: 
                    caminho + nome do arquivo
            
            Retorno:
                None
        """
        self.setFilename(_filename)
        self.setImage(_filename)

    def getImage(self):
        """
        Método que retorna o objeto Image (PIL)
        ---------------------------------------

        Parametros:
            None

        Retorno:
            Image object from PIL
        """
        return self.image
    
    def getFilename(self):
        """
        Método que retorna o diretório + nome do arquivo
        ------------------------------------------------

        Parametros:
            None

        Retorno:
            Image caminho + nome do arquivo
        """
        return self.filename

    #cria uma instancia virtual da imagem(copia ela pra memoria)
    def setImage(self, _filename, memory=False):
        """
        Método que realiza instanciação da imagem em memoria
        ---------------------------------------

        Parametros:
            _filename :  
                Diretório + Nome do arquivo

            
            memory (padrão=False) : 
                parametro que determina se irá abrir  
                diretamente da memoria, ou se apenas irá realizar a atribuição do  
                valor em memoria para o atributo.  

        Retorno:
            Image object from PIL
        """
        if memory:
            self.image = _filename
        else:
            self.image = cv.imread(_filename)
            aux = self.image.copy()
            aux = cv.cvtColor(aux, cv.COLOR_BGR2GRAY)
            ret, self.binaryImage = cv.threshold(aux, 240, 255, cv.THRESH_BINARY)
            del aux, ret


    def setFilename(self, _filename):
        """
        Método que atribui o Caminho + Nome do Arquivo
        ------------------------------------------------

        Parametros:
            _filename: Caminho + Nome do Arquivo

        Retorno:
            None
        """
        self.filename = _filename

    def find_next_non_white_pixel(self, image, x, y):
        """
        Função que procura o pixel não branco mais proximo.
        ------------------------------------------------

        Parâmetros:\n
            \timage:
                \tmatrix (np.asarray) da imagem.
            \tx:
                \tposição inicial do pixel, no eixo X.
            \ty:
                \tposição inicial do pixel, no eixo Y.

        Retorno:\n
            \tRetorna uma tupla que contem os indices X e Y 
            \tdo primeiro pixel não branco encontrado.
        """
        i = x
        j = y
        while i < image.shape[0]:
            j = 0
            while j < image.shape[1]:
                if image[i][j] != 255:
                #if image[i][j][0] != 255 or image[i][j][1] != 255 or image[i][j][2] != 255:
                    return (i, j)
                j += 1
            i += 1

    def find_neigh(self, b, c):
        """
        Função que calcula a qual é a posição de C em relação a B(n_0, n_1, ..., n_7)
        -----------------------------------------------------------------------------

        Parâmetros:\n
            \tb:
                \tindice (x, y) do pixel B atual
            \tc:
                \tindice (x, y) do pixel C atual.

        Retorno:\n
            \tretorna um numero que corresponde a posição de C em relação a B.
        """
        k = [c[0] - b[0], c[1] - b[1]]
        return inverse_neighbors[str(k)]

    def eight_neighborhood(self, image, b, c):
        """
        Função que faz C rodar em volta de B, e retorna o 1º pixel diferente de branco.
        ------------------------------------------------------------------------------

        Parâmetros:\n
            \timage:
                \tmatriz que representa a imagem de interece\n
                \tObs.: A matriz está binarizada, ou seja, só possui duas cores(preto e branco).
            \tb:
                \tindice (x, y) que representa um pixel de borda a borda na imagem a ser segmentada.
            \tc:
                \tindice (x, y) que repsenta o pixel que irá girar em torno do pixel B percorrendo um caminho\n
                \tde 8-Vizinhança até achar um ponto diferente de branco. 

        Retorno:\n
            \tRetorna o indice do novo pixel B que está na 8-vizinhança do pixel B anterior.\n
            \tE o indice do novo pixel C, que é o vizinho anterior ao B (n_0, n_1, ..., n_7). 
        """
        previous_neigh = None
        flag = False
        for i in neighbors:
            if i == 'n_'+str(self.find_neigh(b, c)) or flag:
                flag = True
                x = b[0] + neighbors[i][0]
                y = b[1] + neighbors[i][1]
                if image[x][y] != 255:
                #if image[x][y][0] != 255 or image[x][y][1] != 255 or image[x][y][2] != 255:
                    c[0] = b[0] + previous_neigh[0]
                    c[1] = b[1] + previous_neigh[1]
                    return ([x, y], c)
            previous_neigh = neighbors[i]


        for i in neighbors:
            if i == 'n_'+str(self.find_neigh(b, c)) or flag:
                x = b[0] + neighbors[i][0]
                y = b[1] + neighbors[i][1]
                if image[x][y] != 255:
                #if image[x][y][0] != 255 or image[x][y][1] != 255 or image[x][y][2] != 255:
                    c[0] = b[0] + previous_neigh[0]
                    c[1] = b[1] + previous_neigh[1]
                    return ([x, y], c)
            previous_neigh = neighbors[i]

    #passos 3 a 5 algoritimo
    def explore_frontier(self, image, b, c, end):
        """
        Função que explora a borda de um elemento encontrado
        -----------------------------------------------------------------------------

        Parâmetros:\n
            \timage:
                \tmatriz que representa a imagem de interese.
                \tObs.: a matriz necessita ser binária, ou seja possuir só dois valores, e o objeto de interesse precisa ser preto.
            \tb:
                \tindice (x, y) do pixel B após o b0(inicio da borda)
            \tc:
                \tindice (x, y) do pixel C referente a B.
            \tend:
                \tindice do pixel b0, ou seja, primeiro pixel de borda.

        Retorno:\n
            \tretorna uma lista que contem todos os indices de elementos de fronteira da imagem.
        """
        border = []
        border.append(b)
        
        while not(functools.reduce(lambda i, j : i and j, map(lambda p, q : p == q, border[-1], end), True)):
            b, c = self.eight_neighborhood(image, border[-1], c)
            border.append(b)

        return border


    #passos 1 e 2 do algoritimo
    def segmentation(self, image):
        """
        Função que realiza o processo de segmentação da imagem completa. E grava em disco as imagens segmentadas de borda e da folha completa
        -------------------------------------------------------------------------------------------------------------------------------------

        Parâmetros:\n
            \timage:
                \trecebe uma imagem em memoria(atributo self.image da classe image.py)

        Retorno:\n
            \tnão possui retorno(PODE MUDAR)
        """
        plt.imshow(self.image)
        #plt.show()
        b0 = self.find_next_non_white_pixel(image, 0, 0)
        c0 = [b0[0]-1, b0[1]]

        b, c = self.eight_neighborhood(image, b0, c0)


        frontier = self.explore_frontier(image, b, c, b0)
        frontier.insert(0, b0)
        x = []
        y = []
        for i in frontier:
            x.append(i[0])
            y.append(i[1])

        plt.plot(y, x) 
        self.cropAndSave(self.getImage(), min(x), min(y), max(x), max(y))

        width = max(x) - min(x)
        height = max(y) - min(y)
        
        self.createNewImage(width, height, frontier, max(x), max(y))


        #print(frontier)

        return frontier

    def createNewImage(self, width, height, frontier, xMax, yMax):
        newImage = np.zeros((height, width))
        
        print(newImage.shape)
        print(height, width)
        i = 0
        j = 0

        while (i < newImage.shape[0]):
            j = 0
            while (j < newImage.shape[1]):
                newImage[i][j] = 255
                j = j + 1
            i = i + 1

        i = 0
        while (i < len(frontier)):
            newImage[yMax-frontier[i][1]-1][xMax-frontier[i][0]-1] = 0
            i+=1
        
        fliped = np.fliplr(newImage)

        #(h, w) = fliped.shape[:2]
        #center = (w / 2, h / 2)
        # rotate the image by 180 degrees
        #M = cv.getRotationMatrix2D(center, 90, 1.0)
        #rotated = cv.warpAffine(fliped, M, (w, h))

        image = cv.rotate(fliped, cv.ROTATE_90_CLOCKWISE) 

        cv.imshow("folhinha", image)
        cv.waitKey(0)
        
        #print(newImage)
        return newImage

    def cropAndSave(self, rgbImage, xMin, yMin, xMax, yMax):
        cropedImage = rgbImage[xMin:xMax, yMin:yMax]
        #cv.imshow("folhinha", cropedImage)
        cv.imwrite("teste.png", cropedImage)
        #cv.waitKey(0)
        