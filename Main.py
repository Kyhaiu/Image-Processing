#!/usr/bin/env python
import os
import Screen as sc
import Image  as img
import PySimpleGUI as sg
import numpy as np
import copy

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
                if values['-FILEBROWSE1-'] == '':
                    continue
                else:
                    self.imgs[0] = self.ReadImage(values['-FILEBROWSE1-'])
                    thumb = self.imgs[0].generate_thumbnail(self.imgs[0], first=True)
                    screen.updateLayoutComponents('thumbnail_image_1', thumb)

                    resolution_tmp = '(' + str(self.imgs[0].getResolution()[0]) + 'x' + str(self.imgs[0].getResolution()[1]) + ')'
                    bits_tmp = str(self.imgs[0].getMode()[0]) + '-bit'

                    window.FindElement('-NOT-IMG1-').Update(False)
                    window.FindElement('-SIZE-IMG1-').Update(value = resolution_tmp)
                    window.FindElement('-BIT-DEPTH-IMG1-').Update(value = bits_tmp)
            elif event == '-FILEBROWSE2-':
                if values['-FILEBROWSE2-'] == '':
                    continue
                else:
                    self.imgs[1] = self.ReadImage(values['-FILEBROWSE2-'])
                    thumb = self.imgs[1].generate_thumbnail(self.imgs[1], first=True)
                    screen.updateLayoutComponents('thumbnail_image_2', thumb)

                    resolution_tmp = '(' + str(self.imgs[1].getResolution()[0]) + 'x' + str(self.imgs[1].getResolution()[1]) + ')'
                    bits_tmp = str(self.imgs[1].getMode()[0]) + '-bit'
                    
                    window.FindElement('-NOT-IMG2-').Update(False)
                    window.FindElement('-SIZE-IMG2-').Update(resolution_tmp)
                    window.FindElement('-BIT-DEPTH-IMG2-').Update(bits_tmp)

            #Caso o usuário tenha selecionado a checkbox not da img1 ou img2
            if event == '-NOT-IMG1-' and self.imgs[0] != None:
                aux = img.Image()
                self.imgs[0] = aux.not_operation(self.imgs[0], isinput=True)
                thumb = self.imgs[0].generate_thumbnail(self.imgs[0], first=True)
                screen.updateLayoutComponents('thumbnail_image_1', thumb)

            elif event == '-NOT-IMG1-' and self.imgs[0] == None:
                window.FindElement('-NOT-IMG1-').Update(False)
            
            elif event == '-NOT-IMG2-' and self.imgs[1] != None:
                aux = img.Image()
                self.imgs[1] = aux.not_operation(self.imgs[1], isinput=True)
                thumb = self.imgs[1].generate_thumbnail(self.imgs[1], first=True)
                screen.updateLayoutComponents('thumbnail_image_2', thumb)
            
            elif event == '-NOT-IMG2-' and self.imgs[1] == None:
                window.FindElement('-NOT-IMG2-').Update(False)

            #Caso as duas imagens tenham sido importadas ele executa a operação selecionada
            if self.imgs[0] and self.imgs[1] != None:
                aux = None

                if event == '-APPLYOP-':
                    aux = img.Image()
                    operations = values


                    del operations['-FILEBROWSE1-'], operations['-FILEBROWSE2-'], operations['Abrir Imagem'], operations['Abrir Imagem0']

                    #se o usuário tiver selecionado a operação not no resultado ele tem que negar o valor do proprio resultado para isso passa duas copias dele mesmo
                    if values['-NOT-']:
                        self.imgs[2] = aux.apply_operations(self.imgs[2], self.imgs[2], operations)
                    else:
                        self.imgs[2] = aux.apply_operations(self.imgs[0], self.imgs[1], operations)

                    img_temp = copy.deepcopy(self.imgs[2])
                    thumb = aux.generate_thumbnail(img_temp, first=True)

                    resolution_tmp = '(' + str(self.imgs[2].getResolution()[0]) + 'x' + str(self.imgs[2].getResolution()[1]) + ')'
                    bits_tmp = str(self.imgs[2].getMode()[0]) + '-bit'
                    window.FindElement('-SIZE-IMG-RESULT-').Update(resolution_tmp)
                    window.FindElement('-BIT-DEPTH-RESULT-').Update(bits_tmp)

                    screen.updateLayoutComponents('thumbnail_image_result', thumb)
                    window.FindElement('-SAVE-').Update(disabled=False)
                    del operations, aux, thumb
            elif self.imgs[0] == None and self.imgs[1] == None and event == '-APPLYOP-':
                sg.popup_error('Erro!', 'Por favor realiza a importação da Imagem 1 e Imagem 2 antes de realizar qualquer operação!')

            elif self.imgs[0] == None and event == '-APPLYOP-':
                sg.popup_error('Erro!', 'Por favor realiza a importação da Imagem 1 antes de realizar qualquer operação!')

            elif self.imgs[1] == None and event == '-APPLYOP-':
                sg.popup_error('Erro!', 'Por favor realiza a importação da Imagem 2 antes de realizar qualquer operação!')

            #caso o usuário tenha clicado em salvar e a img resultado for diferente de None 
            if event == "-FILESAVE-" and self.imgs[2] != None:
                path = values['-SAVE-']
                extension = path[int(len(path)-4): len(path)+1 :]
                #trata o caso do usuário tentar salvar um arquivo com qualquer outro formato
                if extension != '.bmp':
                    #if the user inform a invalid file extension, then program returns a error alert
                    sg.popup_error('Erro!', 'Por favor Salve o arquivo resultado com o formato .bmp')
                    continue
                elif path == '':
                    #se o usuário clicar em salvar e decidir cancelar, isso evita da tela quebrar
                    continue

                #salva a img no caminho selecioando
                self.imgs[2].getImage().save(path)
                #self.imgs[2].getImage().convert('RGB').save(path)

            if event == sg.WIN_CLOSED:
                break
        window.close()

    # Função que faz a leitura das imagens
    def ReadImage(self, path):
        replace_path = path.replace("/", "\\\\")
        image = img.Image()
        image.setImage(replace_path)
        """ 
            atributo da classe Image.py Mode = Modo de cor ('1', 'L', 'P', 'RGB')
                '1'   - Imagem     com 1 bit   de resolução de cor
                'L'   - GrayScale  com 8 bits  de resolução de cor
                'P'   - Coloful    com 8 bits  de resolução de cor
                'RGB' - True Color com 24 bits de resolução de cor
        """
        image.setMode(image.getImage().mode)
        image.setResolution(image.getImage().size)
        image.setFileName(os.path.basename(replace_path))
        image.separate_RGB_Channels(image)
        return image

main = Main()
main.StartScreen()