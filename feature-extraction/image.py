from PIL import Image as pil

class image:
    #Construtor da classe
    def __init__(self, _filename):
        self.setFilename(_filename)
        self.setImage(_filename)

    
    #retorna a instancia da imagem
    def getImage(self):
        return self.image
    
    #retorna o caminho + nome da imagem
    def getFilename(self):
        return self.filename

    #cria uma instancia virtual da imagem(copia ela pra memoria)
    def setImage(self, _filename, from_memory=False):
        if from_memory:
            self.image = _filename
        else:
            self.image = pil.open(_filename)

    #armazena o caminho + nome da imagem
    def setFilename(self, _filename):
        self.filename = _filename

    #função cria uma cópia da imagem preto e banca
    def convert_to_binary_image(self, _image, copy=True):
        #se o parametro copia estiver como true, ele cria uma copia do objeto, caso contrario, opera o objeto por referencia
        if copy:
            _image = _image.copy()
        
        #converte a imagem para o mobo binarios
        return _image.convert('1')

    def segmentation(self, image):
        pass