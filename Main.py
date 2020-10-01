import Screen as scrn
import PySimpleGUI as sg

class Main:
    def __init__(self):
        layout = [
            [sg.Text('Selecionar Arquivo: ', size=(15, 1), auto_size_text=False, pad=((10,5),(20,10))),
             sg.InputText('Importar Imagem 1', key='file1', disabled=True, text_color='black', pad=((5,10),(20,10))),
             sg.FileBrowse(button_text='Import', tooltip='HELPZIN', pad=((5,10),(20,10)))],
            [sg.Text('Selecionar Arquivo: ', size=(15, 1), auto_size_text=False, pad=((10,5),(20,10))),
             sg.InputText('Importar Imagem 2', key='file2', disabled=True, text_color='black', pad=((5,10),(20,10))),
             sg.FileBrowse(button_text='Import', tooltip='HELPEZIN', pad=((5,10),(20,10)))],
            [sg.Button('Próxima Etapa', size=(20,1), pad=((10, 5), (20, 10)))]
        ]
        #Janela
        scr = scrn.Screen(None, layout, 'Teste')
        self.screen = scr.getScreen()
    
    def Iniciar(self):  
        while True: 
            #Extrair informações da tela
            self.button, self.values = self.screen.Read()
            if self.button == 'Ajuda - F1':
                sg.popup_error('Error 0x678A', 'File Ajuda.pdf not found in C:/Users/Marcos/Desktop/Projetos/Arquivos Projeto Olguin/Programa')
                continue
            caminho = self.values['caminhoArquivo']
            metodo1 = self.values['metodo1']
            if caminho != 'Importar arquivo(.csv)' and caminho.find('.CSV') != -1:
                if metodo1 == True:
                    pass
                else:
                    pass
            else:
                sg.popup_error('Erro!', 'Por favor realize a importação do Arquivo ".CSV"')
screen = Main()
screen.Iniciar()