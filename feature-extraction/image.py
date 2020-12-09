from PIL import Image as pil

class image:
    #Construtor da classe
    def __init__(self):
        pass
    
    #retorna a instancia da imagem
    def getImage(self):
        return self.image
    
    #retorna o caminho + nome da imagem
    def getFilename(self):
        return self.filename

    #cria uma instancia virtual da imagem(copia ela pra memoria)
    def setImage(self, _filename):
        self.image = pil.open(_filename)

    #armazena o caminho + nome da imagem
    def setFilename(self, _filename):
        self.filename = _filename