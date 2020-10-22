#!/usr/bin/env python
import Screen as sc
import Image  as img
import PySimpleGUI as sg

class Main:
    # Lista de imagens
    imgs = []
    
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
                self.imgs.append(self.ReadImage(values['folderImg1']))
                self.SeparateChannels(0)
            if event == 'folderImg2':
                self.imgs.append(self.ReadImage(values['folderImg2']))
                self.SeparateChannels(1)

            if event == sg.WIN_CLOSED:
                break
        window.close()

    # Função que faz a leitura das imagens
    def ReadImage(self, path):
        image = img.Image()
        image.setImage(path)
        return image

    # Função que faz a separação dos canais RGB pra cada pixel
    def SeparateChannels(self, position):
        self.imgs[position].separate_RGB_Channels()
        
main = Main()
main.StartScreen()