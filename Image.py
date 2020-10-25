import io
import os
import numpy as np
from PIL import Image as pil
from PIL import ImageTk

class Image:
    def __init__(self):
        pass
    
    def getImage(self):
        return self.image

    def getFileName(self):
        return self.filename

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
    
    def setResolution(self, _resolution):
        self.resolution = _resolution

    def setRedChannel(self, _redChannel):
        self.redChannel = _redChannel

    def setGreenChannel(self, _greenChannel):
        self.greenChannel = _greenChannel
        
    def setBlueChannel(self, _blueChannel):
        self.blueChannel = _blueChannel

    def separate_RGB_Channels(self):
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

    def generate_thumbnail(self, _img, first = False):
        """Generate image data using PIL
        """
        rgb_img = _img.getImage().convert('RGB')
        arr = np.asarray(rgb_img)
        maxsize = (320, 320)
        img = pil.fromarray(arr)
        img.thumbnail(maxsize)

        if first:                     # tkinter is inactive the first time
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
            
        del maxsize, arr, rgb_img
        return ImageTk.PhotoImage(img)

    def apply_operations(self, _img1, _img2, _ops):
        if _ops['-ADD-']:
            self.add_operation(_img1, _img2)
        elif _ops['-SUB-']:
            self.sub_operation(_img1, _img2)
        elif _ops['-MUL-']:
            self.mult_operation(_img1, _img2)
        elif _ops['-DIV-']:
            self.div_operation(_img1, _img2)
        elif _ops['-AND-']:
            self.and_operation(_img1, _img2)
        elif _ops['-OR-']:
            self.or_operation(_img1, _img2)
        elif _ops['-NOT-']:
            self.not_operation(_img1)
        return _img1

    def add_operation(self, _img1, _img2):
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()
        print(r1, r2, g1, g2, b1, b2)

    def sub_operation(_img1, _img2):
        print("Subtração")

    def mult_operation(_img1, _img2):
        print("Multiplicação")

    def div_operation(_img1, _img2):
        print("Divisão")

    def and_operation(_img1, _img2):
        print("AND")

    def or_operation(_img1, _img2):
        print("OR")

    def not_operation(_img1):
        print("NOT")