import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import functools

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
            self.image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
            ret, self.image = cv.threshold(self.image, 127, 255, cv.THRESH_BINARY)
            

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
        k = [c[0] - b[0], c[1] - b[1]]
        return inverse_neighbors[str(k)]

    def eight_neighborhood(self, image, b, c):
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
        border = []
        border.append(b)
        
        while not(functools.reduce(lambda i, j : i and j, map(lambda p, q : p == q, border[-1], end), True)):
            b, c = self.eight_neighborhood(image, border[-1], c)
            border.append(b)
            print(f"Cor do pixel {border[-1]} = {image[border[-1][0]][border[-1][1]]}")

        return border


    #passos 1 e 2 do algoritimo
    def segmentation(self, image):
        plt.imshow(self.image)
        plt.show()
        b0 = self.find_next_non_white_pixel(image, 0, 0)
        c0 = [b0[0]-1, b0[1]]

        b, c = self.eight_neighborhood(image, b0, c0)

        border = self.explore_frontier(image, b, c, b0)
        border.insert(0, b0)
        return border

        