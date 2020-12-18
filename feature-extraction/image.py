# https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches

import os
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import functools
import copy
from scipy import ndimage
from math import cos, sin

neighbors = {
    "n_0": [0, -1],
    "n_1": [-1, -1],
    "n_2": [-1,  0],
    "n_3": [-1,  1],
    "n_4": [0,  1],
    "n_5": [1,  1],
    "n_6": [1,  0],
    "n_7": [1, -1]
}

inverse_neighbors = {
    "[0, -1]": 0,
    "[-1, -1]": 1,
    "[-1, 0]": 2,
    "[-1, 1]": 3,
    "[0, 1]": 4,
    "[1, 1]": 5,
    "[1, 0]": 6,
    "[1, -1]": 7
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

    # cria uma instancia virtual da imagem(copia ela pra memoria)
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
            ret, self.image = cv.threshold(
                self.image, 240, 255, cv.THRESH_BINARY)

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
                    # if image[i][j][0] != 255 or image[i][j][1] != 255 or image[i][j][2] != 255:
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
                    # if image[x][y][0] != 255 or image[x][y][1] != 255 or image[x][y][2] != 255:
                    c[0] = b[0] + previous_neigh[0]
                    c[1] = b[1] + previous_neigh[1]
                    return ([x, y], c)
            previous_neigh = neighbors[i]

        for i in neighbors:
            if i == 'n_'+str(self.find_neigh(b, c)) or flag:
                x = b[0] + neighbors[i][0]
                y = b[1] + neighbors[i][1]
                if image[x][y] != 255:
                    # if image[x][y][0] != 255 or image[x][y][1] != 255 or image[x][y][2] != 255:
                    c[0] = b[0] + previous_neigh[0]
                    c[1] = b[1] + previous_neigh[1]
                    return ([x, y], c)
            previous_neigh = neighbors[i]

    # passos 3 a 5 algoritimo
    def explore_frontier(self, image, b, c, end):
        border = []
        border.append(b)

        while not(functools.reduce(lambda i, j: i and j, map(lambda p, q: p == q, border[-1], end), True)):
            b, c = self.eight_neighborhood(image, border[-1], c)
            border.append(b)

        return border

    # passos 1 e 2 do algoritimo

    def segmentation(self, image):
        plt.imshow(self.image)
        # plt.show()
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
        plt.show()
        """
        #Código abaixo tenta salvar uma img nova, mas não está funcioando
        
        frontier_matrix = np.array(frontier)

        # define dimensões da sub-imagem
        min_y = np.min(frontier_matrix[:,0])
        max_y = np.max(frontier_matrix[:,0])
        min_x = np.min(frontier_matrix[:,1])
        max_x = np.max(frontier_matrix[:,1])
        frontier_height = max_y - min_y
        frontier_width  = max_x - min_x

        # padding de 1 ao redor da fronteira
        new_height = frontier_height+1
        new_width = frontier_width+1
        border_img = np.zeros((new_height, new_width))

        # reposiciona as coordernadas de frontier_matrix para o canto superior esquerdo
        frontier_matrix = frontier_matrix - [min_y, min_x]

        # transfere a fronteira para "border_img"
        for f in frontier_matrix:
            border_img[f[0], f[1]] = 1
        
        # cria máscar "mask" que será utilizada para extrair a sub-imagem da imagem original
        mask = copy.deepcopy(border_img)
        mask = ndimage.binary_fill_holes(mask).astype(int)

        # adiciona 3ª dimensão em mask3D para que o broadcast seja possível
        mask3D = np.zeros((new_height, new_width, 1))
        # pega os valores de mask
        mask3D[:,:,0] = mask
        # converte mask3D em uma matriz booleana
        mask3D = np.array(mask3D, dtype=bool)
        
        # aplica máscara "mask" sobre a imagem original, extraindo a subimagem "new_img"
        new_img = np.zeros((new_height, new_width,3))
        new_img = np.multiply(image[min_y:max_y+1, min_x:max_x+1], mask3D)
        img[min_y:max_y+1, min_x:max_x+1,:] = np.multiply(image[min_y:max_y+1, min_x:max_x+1], np.logical_not(mask3D))

        # troca fundos pretos da aplicação da máscara por fundos brancos
        new_img = np.where(mask3D==[0],[255,255,255], new_img)
        img_part = np.where(mask3D==[0], image[min_y:max_y+1, min_x:max_x+1], [255,255,255])
        img[min_y:max_y+1, min_x:max_x+1] = img_part
              
        # transforma imagem de borda em imagem RGB
        # determina os valores de "border_rgb", trocando fundo preto da imagem de borda por fundo branco e deixa o contorno preto
        border_test = np.where(border_img==0, 255, 0)
        border_rgb = np.stack((border_test, border_test, border_test),axis=-1)

        # pega o perimetro da sub-imagem
        perimeter = len(frontier)

        cv.imwrite('Entradas/teste.png', new_img)

        """

        return frontier

    def grayscale(self, image):
        image = cv.imread(
            "C:\\Users\\Sharkb8i_\\Desktop\\FACUL\\PID\\Trabalho #1\\Image-Processing\\feature-extraction\\images\\Entradas\\Teste01.png")
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # Change the current directory to specified directory
        os.chdir("C:\\Users\\Sharkb8i_\\Desktop\\FACUL\\PID\\Trabalho #1\\Image-Processing\\feature-extraction\\images\\Grayscale")
        cv.imwrite("Teste01Gray.png", gray)

        #cv.imshow('Original Image', image)
        #cv.imshow('Gray Image', gray)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

    def glmc(self, image, distances, angles, levels=None, symmetric=False):
        image = np.ascontiguousarray(image)

        image_max = image.max()         # Maior tom de cor que existe na imagem

        """
            O argumento de níveis (levels) é necessário para tipos de dados diferentes
            de uint8. A matriz resultante terá pelo menos níveis 2 de tamanho.
            
            O valor máximo da escala de cinza na imagem deve ser menor que o número de níveis (levels).
        """
        if levels is None:
            levels = 256

        distances = np.ascontiguousarray(distances, dtype=np.float64)
        angles = np.ascontiguousarray(angles, dtype=np.float64)

        P = np.zeros((levels, levels, len(distances), len(angles)),
                    dtype=np.uint32, order='C')

        # Contagem de co-ocorrências
        self.glcm_loop(image, distances, angles, levels, P)

        # Faça cada GLMC simétrico
        if symmetric:
            Pt = np.transpose(P, (1, 0, 2, 3))
            P = P + Pt

        return P

    def glcm_loop(self, image, distances, angle, levels, out):
        rows = image.shape[0]
        cols = image.shape[1]

        a = 0

        for d in range(distances.shape[0]):
            distance = distances[d]
            offset_row = round(sin(angle) * distance)
            offset_col = round(cos(angle) * distance)
            start_row = max(0, -offset_row)
            end_row = min(rows, rows - offset_row)
            start_col = max(0, -offset_col)
            end_col = min(cols, cols - offset_col)
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    i = image[r, c]
                    # Calcula a localização do pixel de deslocamento
                    row = r + offset_row
                    col = c + offset_col
                    j = image[row, col]
                    if 0 <= i < levels and 0 <= j < levels:
                        out[i, j, d, a] += 1

        # https://www.mathworks.com/help/images/ref/referenceetoh36.gif


    # Correlação, contraste e uniformidade
    def glcmprops(self, greylevel, prop='contrast'):
        # 'contrast': sum_{i,j=0}^{levels-1} P_{i,j}(i-j)^2`
        # 'homogeneity': sum_{i,j=0}^{levels-1}frac{P_{i,j}}{1+(i-j)^2}`
        # 'correlation': sum_{i,j=0}^{levels-1} P_{i,j}left[frac{(i-mu_i)(j-mu_j)}{sqrt{(sigma_i^2)(sigma_j^2)}}right]
        pass