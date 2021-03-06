import io
import os
import math
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

    def getMode(self):
        return self.mode

    def getRedChannel(self):
        return self.redChannel

    def getGreenChannel(self):
        return self.greenChannel

    def getBlueChannel(self):
        return self.blueChannel
    
    def setImage(self, _filename=None, from_file=True):
        if not(from_file):
            #in this case filename, is the PIL Image Object
            self.image = _filename
        else:
            #otherwise filename is just filename
            self.image = pil.open(_filename)

    def setFileName(self, _filename):
        self.filename = _filename
    
    def setResolution(self, _resolution):
        #Resolução da imagem (width, height)
        self.resolution = _resolution

    def setMode(self, _mode):
        #salva uma tupla contendo a qtd de bits usados na resolução de cores e a string que representa o modo(ver Mode in Pillow)
        if _mode == '1':
            self.mode = (1, '1')
        elif _mode == 'L':
            self.mode = (8, 'L')
        elif _mode == 'P':
            self.mode = (8, 'P')
        elif _mode == 'RGB':
            self.mode = (24, 'RGB')
        elif _mode == 'RGBA':
            self.mode = (24, 'RGBA')

    def setRedChannel(self, _redChannel):
        self.redChannel = _redChannel

    def setGreenChannel(self, _greenChannel):
        self.greenChannel = _greenChannel
        
    def setBlueChannel(self, _blueChannel):
        self.blueChannel = _blueChannel

    def separate_RGB_Channels(self, _img):
        img = self.getImage()

        # Converte a imagem para 'RGB'
        rgb_img = img.convert('RGB')

        r, g, b =  [], [], []
        width, height = rgb_img.size
        self.setResolution((width, height))
        i = 0
        j = 0

        while i < width:
            while j < height:
                # Separa os canais RGBs em listas (com PIL)
                r.append(rgb_img.getpixel((i, j))[0])
                g.append(rgb_img.getpixel((i, j))[1])
                b.append(rgb_img.getpixel((i, j))[2])
                j+=1
            j=0
            i+=1

        self.setRedChannel(r)
        self.setGreenChannel(g)
        self.setBlueChannel(b)

    def generate_thumbnail(self, _img, first = False):
        """Generate image data using PIL
        """
        maxsize = (320, 320)
        img = _img.getImage()
        img.thumbnail(maxsize)
        if first:                     # tkinter is inactive the first time
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()

        return ImageTk.PhotoImage(img)

    def normalize(self, r, g, b):
        fmax, fmin = max(max(r), max(g), max(b)), min(min(r), min(g), min(b))
        faux = 0
        if (fmax - fmin) <= 0:
            faux = 1
        else:
            faux = fmax - fmin
        auxR = [np.uint8(((255/(faux))*(i - fmin))) for i in r]
        auxG = [np.uint8(((255/(faux))*(i - fmin))) for i in g]
        auxB = [np.uint8(((255/(faux))*(i - fmin))) for i in b]
        del fmin, fmax
        return (auxR, auxG, auxB)

    def create_img_from_matrix(self, _matrix, _img1, _img2):
        #funcção que cria uma imagem a partir de uma matrix de pixels
        #lembrando que a operação not, seja nos inputs ou resultado são criados a partir de valores da memoria
        img = Image()
        depth_img_1 = _img1.getMode()
        depth_img_2 = _img2.getMode()
        
        #Ele verifica qual é a maior resolução de cores e salva a img resultante conforme a maior resolução
        if depth_img_1[0] >= depth_img_2[0]:
            img.setImage(pil.frombytes('RGB', (_matrix.shape[0], _matrix.shape[1]), _matrix, decoder_name="raw").transpose(pil.TRANSPOSE).convert(depth_img_1[1]), from_file=False)
            img.setMode(depth_img_1[1]) 
        else:
            img.setImage(pil.frombytes('RGB', (_matrix.shape[0], _matrix.shape[1]), _matrix, decoder_name="raw").transpose(pil.TRANSPOSE).convert(depth_img_2[1]), from_file=False)
            img.setMode(depth_img_2[1]) 
               
        img.setResolution(img.getImage().size)
        img.separate_RGB_Channels(img)

        return img

    def apply_operations(self, _img1, _img2, _ops):
        img_temp = Image()
        if _ops['-ADD-']:
            img_temp = self.add_operation(_img1, _img2)
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
        elif _ops['-XOR-']:
            img_temp = self.xor_operation(_img1, _img2)
        elif _ops['-NOT-'] or _ops['-NOT-IMG1-'] or _ops['-NOT-IMG2-']:
            img_temp = self.not_operation(_img1)

        img_temp = self.create_img_from_matrix(img_temp, _img1, _img2)
        return img_temp

    def add_operation(self, _img1, _img2):
        arr_img_result = None

        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()

        temp_r = [int(x) + int(y) for x, y in zip(r1, r2)]
        temp_g = [int(x) + int(y) for x, y in zip(g1, g2)]
        temp_b = [int(x) + int(y) for x, y in zip(b1, b2)]

        temp_r, temp_g, temp_b = self.normalize(temp_r, temp_g, temp_b)

        arr_img_result = np.dstack([temp_r, temp_g, temp_b])
        arr_img_result = np.asarray(arr_img_result)
        arr_img_result = arr_img_result.reshape(min(_img1.getResolution()[0], _img2.getResolution()[0]), min(_img1.getResolution()[1], _img2.getResolution()[1]), 3)

        return arr_img_result

    def sub_operation(self, _img1, _img2):
        arr_img_result = None

        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()

        temp_r = [int(x) - int(y) for x, y in zip(r1, r2)]
        temp_g = [int(x) - int(y) for x, y in zip(g1, g2)]
        temp_b = [int(x) - int(y) for x, y in zip(b1, b2)]

        temp_r, temp_g, temp_b = self.normalize(temp_r, temp_g, temp_b)

        arr_img_result = np.dstack([temp_r, temp_g, temp_b])
        arr_img_result = np.asarray(arr_img_result)

        arr_img_result = arr_img_result.reshape(min(_img1.getResolution()[0], _img2.getResolution()[0]), min(_img1.getResolution()[1], _img2.getResolution()[1]), 3)

        return arr_img_result

    def mult_operation(self, _img1, _img2):
        arr_img_result = None

        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()

        temp_r = [int(x) * int(y) for x, y in zip(r1, r2)]
        temp_g = [int(x) * int(y) for x, y in zip(g1, g2)]
        temp_b = [int(x) * int(y) for x, y in zip(b1, b2)]

        temp_r, temp_g, temp_b = self.normalize(temp_r, temp_g, temp_b)

        arr_img_result = np.dstack([temp_r, temp_g, temp_b])
        arr_img_result = np.asarray(arr_img_result)

        arr_img_result = arr_img_result.reshape(min(_img1.getResolution()[0], _img2.getResolution()[0]), min(_img1.getResolution()[1], _img2.getResolution()[1]), 3)

        return arr_img_result

    def div_operation(self, _img1, _img2):
        arr_img_result = None

        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()

        temp_r = [int(x) / int(y) if (int(y) > 0 ) else int(x) / 1 for x, y in zip(r1, r2)]
        temp_g = [int(x) / int(y) if (int(y) > 0 ) else int(x) / 1 for x, y in zip(g1, g2)]
        temp_b = [int(x) / int(y) if (int(y) > 0 ) else int(x) / 1 for x, y in zip(b1, b2)]

        temp_r, temp_g, temp_b = self.normalize(temp_r, temp_g, temp_b)

        arr_img_result = np.dstack([temp_r, temp_g, temp_b])
        arr_img_result = np.asarray(arr_img_result)

        arr_img_result = arr_img_result.reshape(min(_img1.getResolution()[0], _img2.getResolution()[0]), min(_img1.getResolution()[1], _img2.getResolution()[1]), 3)

        return arr_img_result

    def and_operation(self, _img1, _img2):
        arr_img_result = None

        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()

        temp_r = [int(x) and int(y) for x, y in zip(r1, r2)]
        temp_g = [int(x) and int(y) for x, y in zip(g1, g2)]
        temp_b = [int(x) and int(y) for x, y in zip(b1, b2)]

        temp_r, temp_g, temp_b = self.normalize(temp_r, temp_g, temp_b)

        arr_img_result = np.dstack([temp_r, temp_g, temp_b])
        arr_img_result = np.asarray(arr_img_result)

        arr_img_result = arr_img_result.reshape(min(_img1.getResolution()[0], _img2.getResolution()[0]), min(_img1.getResolution()[1], _img2.getResolution()[1]), 3)

        return arr_img_result

    def or_operation(self, _img1, _img2):
        arr_img_result = None

        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()

        temp_r = [int(x) or int(y) for x, y in zip(r1, r2)]
        temp_g = [int(x) or int(y) for x, y in zip(g1, g2)]
        temp_b = [int(x) or int(y) for x, y in zip(b1, b2)]

        temp_r, temp_g, temp_b = self.normalize(temp_r, temp_g, temp_b)

        arr_img_result = np.dstack([temp_r, temp_g, temp_b])
        arr_img_result = np.asarray(arr_img_result)

        arr_img_result = arr_img_result.reshape(min(_img1.getResolution()[0], _img2.getResolution()[0]), min(_img1.getResolution()[1], _img2.getResolution()[1]), 3)

        return arr_img_result

    def xor_operation(self, _img1, _img2):
        arr_img_result = None

        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()

        temp_r = [int(x) ^ int(y) for x, y in zip(r1, r2)]
        temp_g = [int(x) ^ int(y) for x, y in zip(g1, g2)]
        temp_b = [int(x) ^ int(y) for x, y in zip(b1, b2)]

        temp_r, temp_g, temp_b = self.normalize(temp_r, temp_g, temp_b)

        arr_img_result = np.dstack([temp_r, temp_g, temp_b])
        arr_img_result = np.asarray(arr_img_result)

        arr_img_result = arr_img_result.reshape(min(_img1.getResolution()[0], _img2.getResolution()[0]), min(_img1.getResolution()[1], _img2.getResolution()[1]), 3)

        return arr_img_result

    def not_operation(self, _img1, isinput=False):
        #operação NOT, usanda tanto para as imagens inputs, quanto no resultado
        #parametro isinput serve como flag para ver se não é o NOT das IMG 1 ou IMG2
        arr_img_result = None

        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        width, height = _img1.getResolution()[0], _img1.getResolution()[1]

        temp_r = [~x for x in r1]
        temp_g = [~x for x in g1]
        temp_b = [~x for x in b1]

        temp_r, temp_g, temp_b = self.normalize(temp_r, temp_g, temp_b)

        arr_img_result = np.dstack([temp_r, temp_g, temp_b])
        arr_img_result = np.asarray(arr_img_result)
        arr_img_result = arr_img_result.reshape(width, height, 3)

        if isinput:

            arr_img_result =  self.create_img_from_matrix(arr_img_result, _img1, _img1)

        return arr_img_result