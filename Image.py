import io
import os
import numpy as np
import itertools as it
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
        arr = np.dstack((_img.getRedChannel(), _img.getGreenChannel(), _img.getBlueChannel())) .astype(np.uint8)

        maxsize = (320, 320)
        img = pil.frombytes('L', maxsize, arr)
        img.thumbnail(maxsize)

        if first:                     # tkinter is inactive the first time
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
            
        del maxsize, arr
        return ImageTk.PhotoImage(img)

    def apply_operations(self, _img1, _img2, _ops):
        img_temp = Image()
        if _ops['-ADD-']:
            img_temp = self.add_operation(_img1, _img2)
            return img_temp
        elif _ops['-SUB-']:
            img_temp = self.sub_operation(_img1, _img2)
        elif _ops['-MUL-']:
            img_temp = self.mult_operation(_img1, _img2)
        elif _ops['-DIV-']:
            img_temp = self.div_operation(_img1, _img2)
        elif _ops['-AND-']:
            img_temp = self.and_operation(_img1, _img2)
        elif _ops['-OR-']:
            img_temp = self.or_operation(_img1, _img2)
        elif _ops['-NOT-']:
            img_temp = self.not_operation(_img1)
        return _img1

    def add_operation(self, _img1, _img2):
        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()
        
        # Soma cada canal de cada imagem (lista) com os seus respectivos
        # EX: r[0]_img1 + r[0]_img2
        sum_r = [sum(x) for x in it.zip_longest(r1, r2, fillvalue = 0)]
        i = 0
        while(i < len(sum_r)):
            if(sum_r[i] > 255):
                sum_r[i] = 255
            i+=1

        sum_g = [sum(x) for x in it.zip_longest(g1, g2, fillvalue = 0)]
        i = 0
        while(i < len(sum_g)):
            if(sum_g[i] > 255):
                sum_g[i] = 255
            i+=1

        sum_b = [sum(x) for x in it.zip_longest(b1, b2, fillvalue = 0)]
        i = 0
        while(i < len(sum_b)):
            if(sum_b[i] > 255):
                sum_b[i] = 255
            i+=1

        # Seta os novos canais calculados
        img_temp = Image()
        img_temp.setRedChannel(sum_r)
        img_temp.setGreenChannel(sum_g)
        img_temp.setBlueChannel(sum_b)

        # Desaloca as variaveis
        del r1, r2, sum_r, g1, g2, sum_g, b1, b2, sum_b

        # Retorno do novo objeto Image
        return img_temp

    """
        i = 0
        while i < len(sum_r):
            print(r1[i], r2[i], sum_r[i], g1[i], g2[i], sum_g[i], b1[i], b2[i], sum_b[i])
            os.system("PAUSE")
            i+=1
    """

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