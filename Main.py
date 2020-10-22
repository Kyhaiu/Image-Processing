#!/usr/bin/env python
import io
import os
import numpy as np
import PySimpleGUI as sg
import Screen as sc
from PIL import Image, ImageTk

class Main:
    #Construtor da classe MAIN
    def __init__(self):
       pass

    #função que inicia a execução (E CRIA A TELA)
    def Iniciar(self):
        screen = sc.Screen()
        window = screen.getScreen()
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            print(event, values)
        window.close()

main = Main()
main.Iniciar()