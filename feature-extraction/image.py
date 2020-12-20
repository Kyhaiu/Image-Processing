import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import functools
import copy
from scipy import ndimage
from math import cos, sin

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
    def __init__(self, _path, _filename):
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
        self.setPath(_path)
        self.setImage(_path + '\\' + _filename)
        

    def getPath(self):
        return self.path

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

    def getBinaryImage(self):
        """
        Função que retorna a imagem binária
        -----------------------------------

        Paramentros:
            \tNenhum\n

        Retorno:
            \treturn: Retorna a imagem binária
        """
        return self.binaryImage

    def setPath(self, _path):
        """
        Função que armazena o caminho do arquivo
        ----------------------------------------

        Paramentros:
            \t_path: String que indica o caminho do arquivo

        Retorno:
            \treturn: None
        """
        self.path = _path

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
            self.image = cv.copyMakeBorder(self.image, 1, 1, 1, 1, cv.BORDER_CONSTANT, value=[255, 255, 255])
            aux = self.image.copy()
            aux = cv.cvtColor(aux, cv.COLOR_BGR2GRAY)
            ret, self.binaryImage = cv.threshold(aux, 245, 255, cv.THRESH_BINARY)

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
            if np.mean(image[i]) != 255:
                while j < image.shape[1]:
                    if image[i][j] != 255:
                        return [i, j]
                    j += 1
            i += 1
        return [-1, -1]

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
                    if previous_neigh != None:
                        c[0] = b[0] + previous_neigh[0]
                        c[1] = b[1] + previous_neigh[1]
                    return ([x, y], c)
            previous_neigh = neighbors[i]


        for i in neighbors:
            if i == 'n_'+str(self.find_neigh(b, c)) or flag:
                x = b[0] + neighbors[i][0]
                y = b[1] + neighbors[i][1]
                if image[x][y] != 255:
                    if previous_neigh != None:
                        c[0] = b[0] + previous_neigh[0]
                        c[1] = b[1] + previous_neigh[1]
                    return ([x, y], c)
            previous_neigh = neighbors[i]
        
        return ([-1,-1],-1)

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
    def segmentation(self, image, r, c):
        """
        Função que realiza o processo de segmentação da imagem completa. E grava em disco as imagens segmentadas de borda e da folha completa
        -------------------------------------------------------------------------------------------------------------------------------------

        Parâmetros:\n
            \timage:
                \trecebe uma imagem em memoria(atributo self.image da classe image.py)

        Retorno:\n
            \tnão possui retorno(PODE MUDAR)
        """
        #plt.imshow(self.image)
        #plt.show()
        cont = 1
        b0 = self.find_next_non_white_pixel(image, 0, 0)
        c0 = [b0[0]-1, b0[1]]
        while b0[0] != -1 :

            b, c = self.eight_neighborhood(image, b0, c0)
            if c == -1:
                self.binaryImage[b0[0]][b0[1]] = 255
                b0 = self.find_next_non_white_pixel(image, 0, 0)
                c0 = [b0[0]-1, b0[1]]
                continue

            frontier = self.explore_frontier(image, b, c, b0)
            frontier.insert(0, b0)

            h, w = self.binaryImage.shape[:2]
            if(len(frontier) >= (2*(h-2) + 2*(w-2)) - 4):
                print("here")
                self.floodFill(h, w, frontier[0][1], frontier[0][0])
                b0 = self.find_next_non_white_pixel(image, 0, 0)
                c0 = [b0[0]-1, b0[1]]
                continue

            if len(frontier) <= 100:
                self.removeNoise(frontier)
                b0 = self.find_next_non_white_pixel(image, 0, 0)
                c0 = [b0[0]-1, b0[1]]
                continue

            x = []
            y = []
            for i in frontier:
                x.append(i[0])
                y.append(i[1])


            width = max(x) - min(x)
            height = max(y) - min(y)

                
            self.floodFill(h, w, frontier[0][1], frontier[0][0])
                
            self.saveBorder(width, height, frontier, max(x), max(y), cont)

            self.cropAndSave(self.getImage(), min(x), min(y), max(x), max(y), cont, frontier)
                

            cont+=1
            b0 = self.find_next_non_white_pixel(image, 0, 0)
            c0 = [b0[0]-1, b0[1]]
            
        
    def removeNoise(self, frontier):
        """
        Função que remove ruidos encontrados durante a segmentação
        ----------------------------------------------------------

        Paramentros:
            \tfrontier: Lista de indices (x, y) dos pixels de ruidos a serem removidos\n

        Retorno:
            return: não possui, pois opera diretamente na matriz da imagem binária
        """
        for i in frontier:
            self.binaryImage[i[0]][i[1]] = 255    


    def saveBorder(self, width, height, frontier, xMax, yMax, cont):
        """
        Função que salva a borda da folha segmentada
        -----------------------------------------------------
        Parametros:
            \twidth: Largura da imagem obtido atravéz de xMax - xMin\n
            \theight: Altura da imagem obtida atravéz de yMax - yMin\n
            \tcont: Variavel usada pra salvar com o nome correto\n
            \tfrontier: Array que contem todos os pontos da fronteira\n

        Retorno
        -------
            return: Nada por enquanto
        """
        print("Salvando cópia da borda da folha segmentada.")
        print("Borda : " + self.getFilename().replace(".png","") + str(cont) + "-P.png")
        newImage = np.zeros((height, width))
        
        #print(newImage.shape)
        #print(height, width)
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
    

        image = cv.rotate(fliped, cv.ROTATE_90_CLOCKWISE) 
        cv.imwrite(self.getPath() + "\\" + self.getFilename().replace(".png","") + str(cont) +"-P.png"  , image)

        del fliped, image
        

    def cropAndSave(self, rgbImage, xMin, yMin, xMax, yMax, cont, frontier):
        """
        Função que recorta e salva a folha, com base na borda
        -----------------------------------------------------
        Parametros:
            \trgbImage: Imagem completa colorida\n
            \txMin; yMin: Indices minimos obtidos atravéz da borda\n
            \txMax; yMax: Indices maximos obtidos atravéz da borda\n
            \tcont: Variavel usada pra salvar com o nome correto\n
            \tfrontier: Array que contem todos os pontos da fronteira\n

        Retorno
        -------
            \treturn: Nada por enquanto
        """
        print("Salvando cópia da folha segmentada.")
        print("Folha : " + self.getFilename().replace(".png","") + str(cont) + ".png")
        mask = cv.imread(self.getPath()+"\\"+self.getFilename().replace(".png","") + str(cont) + "-P.png")
        frontier_matrix = np.array(frontier)

        frontier_height = yMax - yMin
        frontier_width  = xMax - xMin
        new_height = frontier_height+1
        new_width = frontier_width+1
        border_img = np.zeros((new_width, new_height), dtype=np.uint8)
        frontier_matrix = frontier_matrix - [xMin, yMin]
        for f in frontier_matrix:
            border_img[f[0], f[1]] = 1
    
        mask = copy.deepcopy(border_img)
        mask = ndimage.binary_fill_holes(mask).astype(int)
        mask3D = np.zeros((new_width, new_height, 1))
        mask3D[:,:,0] = mask
        mask3D = np.array(mask3D, dtype=bool)
        new_img = np.zeros((new_height-1, new_width-1, 3), dtype=np.uint8)
        new_img = np.multiply(self.image[xMin:xMax+1, yMin:yMax+1], mask3D)

        self.image[xMin:xMax+1, yMin:yMax+1,:] = np.multiply(self.image[xMin:xMax+1, yMin:yMax+1], np.logical_not(mask3D))

        new_img = np.where(mask3D==[0],[255,255,255], new_img)
        img_part = np.where(mask3D==[0], self.image[xMin:xMax+1, yMin:yMax+1], [255,255,255])
        self.image[xMin:xMax+1, yMin:yMax+1] = img_part

        perimeter = len(frontier)
        cv.imwrite(self.getPath() + "\\" + self.getFilename().replace(".png","-") + str(cont) +".png"  , new_img)

        del mask, mask3D, img_part

    def floodFill (self, h, w, x, y):
        """
        Função unica e exclusivamente para remover o objeto da imagem binária
        ---------------------------------------------------------------------

        Paramentros:
            \th: Altura da imagem(xMax - xMin)\n
            \tw: Largura da imagem(yMax -yMin)\n
            \tx;y: Indice de onde o floodfill irá começar

        Retorno:
            \treturn: None
        """
        mask = np.zeros((h+2, w+2), np.uint8)

        cv.floodFill(self.binaryImage, mask, (x, y), 255)