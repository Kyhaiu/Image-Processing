#!/usr/bin/env python
import Screen as sc
import Image  as img
import PySimpleGUI as sg
import numpy as np

class Main:
    """
        Lista de imgens:
            - imgs[0] =  Imagem 1
            - imgs[1] =  Imagem 2
            - imgs[2] =  Imagem resultado
    """
    imgs = [None, None, None]

    #Construtor da classe MAIN
    def __init__(self):
       pass

    # Função que seta a tela e inicia
    def StartScreen(self):
        screen = sc.Screen()
        window = screen.getScreen()
        while True:
            event, values = window.read()

            # Leitura das imagens
            if event == 'folderImg1':
                self.imgs[0] = self.ReadImage(values['folderImg1'])
            elif event == 'folderImg2':
                self.imgs[1] = self.ReadImage(values['folderImg2'])

            if self.imgs[0] and self.imgs[1] != None:
                if event == '-APPLYOP-':
                    aux = img.Image()
                    operations = values

                    for i in range(1, 3, 1):
                        del operations['folderImg' + str(i)]
                        del operations['file' + str(i)]

                    self.imgs[2] = aux.apply_operations(self.imgs[0], self.imgs[1], operations)

                    thumb = aux.generate_thumbnail(self.imgs[2], True)

                    screen.updateLayoutComponents('thumbnail', thumb)
                    del operations, aux

            if event == sg.WIN_CLOSED:
                break
        window.close()

    # Função que faz a leitura das imagens
    def ReadImage(self, path):
        image = img.Image()
        image.setImage(path)
        image.separate_RGB_Channels()
        return image

main = Main()
main.StartScreen()