#!/usr/bin/env python
import Screen as sc
import Image  as img
import PySimpleGUI as sg

class Main:
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
                self.PrepareImage(values['folderImg1'])
            if event == 'folderImg2':
                self.PrepareImage(values['folderImg2'])

            if event == sg.WIN_CLOSED:
                break
        window.close()

    # Função que faz a leitura das imagens
    def PrepareImage(self, path):
        image = img.Image()
        image.setImage(path)
        image.separate_RGB_Channels()
        print(image.getRedChannel())    # Print do do canal R de todos os pixels
        print(image.getGreenChannel())  # Print do do canal G de todos os pixels
        print(image.getBlueChannel())   # Print do do canal B de todos os pixels
        
main = Main()
main.StartScreen()