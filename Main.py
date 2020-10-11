#!/usr/bin/env python
import PySimpleGUI as sg
import os
from PIL import Image, ImageTk
import io

class Main:
    #Construtor da classe MAIN
    def __init__(self):
        #Armazena a pasta onde estão localizadas as imagens
        self.setFolder(sg.popup_get_folder('Image folder to open', default_path=''))
        if not self.getFolder():
            #Se o caminho da pasta for vazio então o programa é encerrado
            sg.popup_cancel('Selecione um caminho valido!', title='Erro!')
            raise SystemExit()
        #tipos de imagens suportadas
        self.setImgTypes((".bmp"))
        
        try:
            #tenta pegar a lista de arquivos do diretório
            flist0 = os.listdir(self.getFolder())
        except FileNotFoundError:
            #caso o diretório não exista(caso vc tente alterar o nome do diretório ou coloque o nome de um diretório inválido) o programa encerra
            sg.popup_cancel('O sistema não pode encontrar o caminho especificado.',title='Erro!')
            raise SystemExit()

        #seta a lista de arquivos do diretório
        #para cada 'f' na lista de arquivos('flist0') ele verifica se 'f' é um arquivo do tipo que o programa suporta('img_types') no diretório selecionado
        self.setFileNames([f for f in flist0 if os.path.isfile(os.path.join(self.getFolder(), f)) and f.lower().endswith(self.getImgTypes())])

        #seta no numero de aquivos no diretório(numeros de arquivos que o programa supoerta(img_type))
        self.setNumFiles(len(self.getFileNames()))
        if self.getNumFiles() == 0:
            sg.popup('Não existem arquivos suportados no diretório escolhido', title='Erro!')
            raise SystemExit()
        
        #desaloca flist0
        del flist0

    #getters dos atributos da classe main
    def getFolder(self):
        return self.folder
    
    def getImgTypes(self):
        return self.img_types

    def getFileNames(self):
        return self.fnames
    
    def getNumFiles(self):
        return self.num_files

    #setters dos atributos da classe main
    def setFolder(self, _folder):
        self.folder = _folder

    def setFileNames(self, _fnames):
        self.fnames = _fnames
    
    def setImgTypes(self, _img_types):
        self.img_types = _img_types
    
    def setNumFiles(self, _num_files):
        self.num_files = _num_files

    #esse get pega o arquivo da imagem e gera a thumbnail
    def get_img_data(self, f, maxsize=(1200, 850), first=False):
        """Generate image data using PIL
        """
        img = Image.open(f)
        img.thumbnail(maxsize)
        if first:                     # tkinter is inactive the first time
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
        return ImageTk.PhotoImage(img)

    #função que inicia a execução
    def Iniciar(self):
        #pega o 1° arquivo da lista de aquivos
        filename = os.path.join(self.getFolder(), self.getFileNames()[0])  # name of first file in list
        #componente do PySimpleGUI que exibe a imagem(não da pra manipular os dados, pois é um objt do tipo sg.Image)
        image_elem = sg.Image(data=self.get_img_data(filename, first=True))
        #elemento do PySimpleGUI que exive o nome do arquivo selecionado
        filename_display_elem = sg.Text(filename, size=(80, 3))
        #elemento mostra o numero de arquivos existentes(formatos suportados) na pasta selecionada
        file_num_display_elem = sg.Text('File 1 of {}'.format(self.getNumFiles()), size=(15, 1))

        # exibe o nome do arquivo seleciona e a imagem
        col = [[filename_display_elem],
                [image_elem]]

        #exibe os nomes dos arquivos e os botões 'next' e 'prev'
        col_files = [[sg.Listbox(values=self.getFileNames(), change_submits=True, size=(60, 30), key='listbox')],
                    [sg.Button('Next', size=(8, 2)), sg.Button('Prev', size=(8, 2)), file_num_display_elem]]

        #layout da aplicação
        layout = [[sg.Column(col_files), sg.Column(col)]]

        #método que gera a janela(sepa nem precisa da classe Screen{verificar necessidade futura})
        window = sg.Window('Image Browser', layout, return_keyboard_events=True,
                        location=(0, 0), use_default_focus=False)

        # loop lendo o input do usuário e mostrando a imagem e o nome dela
        i = 0
        while True:
            # lendo os valores apartir do form
            event, values = window.read()
            print(event, values)
            # perform button and keyboard operations
            if event == sg.WIN_CLOSED:
                break
            elif event in ('Next', 'MouseWheel:Down', 'Down:40', 'Next:34'):
                i += 1
                if i >= self.getNumFiles():
                    i -= self.getNumFiles()
                filename = os.path.join(self.getFolder(), self.getFileNames()[i])
            elif event in ('Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33'):
                i -= 1
                if i < 0:
                    i = self.getNumFiles() + i
                filename = os.path.join(self.getFolder(), self.getFileNames()[i])
            elif event == 'listbox':            # something from the listbox
                f = values["listbox"][0]            # selected filename
                filename = os.path.join(self.getFolder(), f)  # read this file
                i = self.getFileNames().index(f)                 # update running index
            else:
                filename = os.path.join(self.getFolder(), self.getFileNames()[i])

            # atualiza a janela com a nova imagem
            image_elem.update(data=self.get_img_data(filename, first=True))
            # atualizaz a janela com o novo nome da imagem
            filename_display_elem.update(filename)
            # atualiza a lista de arquivos
            file_num_display_elem.update('File {} of {}'.format(i+1, self.getNumFiles()))

        window.close()        
screen = Main()
screen.Iniciar()
