import io
import os
import PIL as pil
import numpy as np

class Image:
    def __init__(self):
        pass
    
    def getImage(self):
        return self.image

    def getFileName(self):
        return self.filename

    def getColorMode(self):
        return self.colorMode

    def getResolution(self):
        return self.resolution

    def getRedChannel(self):
        return self.redChannel

    def getGreenChannel(self):
        return self.greenChannel

    def getBlueChannel(self):
        return self.blueChannel
    
    def setImage(self, _filename):
        self.image = pil.open(_filename)

    def setFileName(self, _filename):
        self.filename = _filename

    def setColorMode(self, _colorMode):
        self.colorMode = _colorMode
    
    def setResolution(self, _resolution):
        self.resolution = _resolution

    def setRedChannel(self, _redChannel):
        self.redChannel = _redChannel

    def setGreenChannel(self, _greenChannel):
        self.greenChannel = _greenChannel
        
    def setBlueChannel(self, _blueChannel):
        self.blueChannel = _blueChannel

    def to_separete_rgb(self):
        img = self.getImage()

        # Converte a imagem para 'RGB'
        rgb_img = img.convert('RGB')

        # Passa a imagem rgb para um array
        arr = np.array(rgb_img)

        # Separa os 3 canais com o split
        r, g, b = np.split(arr, 3, axis = 2)
        r = r.reshape(-1)
        g = r.reshape(-1)
        b = r.reshape(-1)
        self.setRedChannel(r)
        self.setGreenChannel(g)
        self.setBlueChannel(b)

        #Desaloca as variaveis
        del img, rgb_img, r, g, b

    def generate_thumbnail(self, f, maxsize=(320, 320), first=False):
        pass
        """tem que montar uma função que consiga gerar uma thumbnail com os valores rgb
            OBS.: essa função só gera uma thumbnail de um arquivo salvo em disco 
        img = pil.open(f)
        img.thumbnail(maxsize)
        if first:                     # tkinter is inactive the first time
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
        return pil.PhotoImage(img)
        """

        