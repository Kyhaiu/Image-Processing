import numpy as np
import functools
from PIL import Image as pil

neighbors = {
            "n_0": [ 0,-1],
            "n_1": [-1,-1],
            "n_2": [-1, 0],
            "n_3": [-1, 1],
            "n_4": [ 0, 1],
            "n_5": [ 1, 1],
            "n_6": [ 1, 0],
            "n_7": [ 1,-1]
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
            self.image = pil.open(_filename)

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

        Parametros:\n
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
                if image[i][j][0] != 255 or image[i][j][1] != 255 or image[i][j][2] != 255:
                    return (i, j)
                j += 1
            i += 1
        return None

    def eight_neighborhood(self, image, x, y):
        for i in neighbors:
            if not(functools.reduce(lambda i, j : i and j, map(lambda p, q : p == q, image[x + (neighbors[i])[0]][y + (neighbors[i])[1]], [255, 255, 255]), True)):
                return (x+(neighbors[i])[0], y+(neighbors[i])[1])

        

            

    def segmentation(self, image):
        """
            Parametros:
                image: Objeto da classe Image(PIL)
            
            Retorno:
                função não retorna nada, irá realizar a segmentação da imagem e salvar as imagens individuais
                na pasta ./imagens/Saida com o nome 

            Algoritimo seguidor de fronteira(Representação e Fronteira Slide 4)

            1)  b0 é o ponto de borda(1) de partida(mais alto à esquerda) c0 (0) é o vizinho a oeste de b0.
                Examina a vizinhança-8 de b0 a partir de c0 no sentido horário. b1 é o primeiro vizinho encontrado
                com valor 1 e c1(0) é o vizinho anterior. Guarde a localização de b0 e b1 para a etapa 5;

            2)  Considere b = b1 e c = c1;

            3)  Faça com que os vizinhos-8 de b, a partir de c em sentido horarío, sejam indicados por n1, n2, ..., n8. Encontro o primeiro nk de borda(1)

            4)  Considere b = nk e c = nk-1

            5)  Repita 3) e 4) até que b = b0 e o próximo ponto de fronteira encontrado seja b1. 
                A sequência de pontos b encontrados quando encerrado o algorimo constituem o conjunto de ponto de fronteira ordenados.
        """
        img_arr = np.asarray(image.copy())
        b= []
        b.append(self.find_next_non_white_pixel(img_arr, 0, 0))
        print(b)

        b_aux= (None, None)
        b_aux= self.eight_neighborhood(img_arr, b[-1][0], b[-1][1])
        b.append(b_aux)
        
        while b[-1] != b[0]:
            b_aux= self.eight_neighborhood(img_arr, b[-1][0], b[-1][1])
            #adicionei essa linha
            img_arr[b[-1][0]][b[-1][1]] = [255, 255, 255]
            b.append(b_aux)
        
        print(b)

        