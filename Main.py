#!/usr/bin/env python
import os
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
            if event == '-FILEBROWSE1-':
                self.imgs[0] = self.ReadImage(values['-FILEBROWSE1-'])
                thumb = self.imgs[0].generate_thumbnail(self.imgs[0], first=True)
                screen.updateLayoutComponents('thumbnail_image_1', thumb)
            elif event == '-FILEBROWSE2-':
                self.imgs[1] = self.ReadImage(values['-FILEBROWSE2-'])
                thumb = self.imgs[1].generate_thumbnail(self.imgs[1], first=True)
                screen.updateLayoutComponents('thumbnail_image_2', thumb)

            if event == '-NOT-IMG1-' and self.imgs[0] != None:
                    aux = img.Image()
                    self.imgs[0] = aux.not_operation(self.imgs[0], isinput=True)
                    thumb = self.imgs[0].generate_thumbnail(self.imgs[0], first=True)
                    screen.updateLayoutComponents('thumbnail_image_1', thumb)
            elif event == '-NOT-IMG2-' and self.imgs[1] != None:
                aux = img.Image()
                self.imgs[1] = aux.not_operation(self.imgs[1], isinput=True)
                thumb = self.imgs[1].generate_thumbnail(self.imgs[1], first=True)
                screen.updateLayoutComponents('thumbnail_image_2', thumb)

            if self.imgs[0] and self.imgs[1] != None:
                aux = None

                if event == '-APPLYOP-':
                    aux = img.Image()
                    operations = values

                    del operations['-FILEBROWSE1-'], operations['-FILEBROWSE2-'], operations['Abrir Imagem'], operations['Abrir Imagem0']

                    if values['-NOT-']:
                        self.imgs[2] = aux.apply_operations(self.imgs[2], None, operations)
                    else:
                        self.imgs[2] = aux.apply_operations(self.imgs[0], self.imgs[1], operations)

                    thumb = aux.generate_thumbnail(self.imgs[2], first=True)

                    screen.updateLayoutComponents('thumbnail_image_result', thumb)
                    del operations, aux

            if event == sg.WIN_CLOSED:
                break
        window.close()

    # Função que faz a leitura das imagens
    def ReadImage(self, path):
        replace_path = path.replace("/", "\\\\")
        image = img.Image()
        image.setImage(replace_path)
        image.setFileName(os.path.basename(replace_path))
        image.separate_RGB_Channels(image)
        return image

main = Main()
main.StartScreen()