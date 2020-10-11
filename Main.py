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
    def get_img_data(self, f, maxsize=(320, 320), first=False):
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
        #elemento mostra o numero de arquivos existentes(formatos suportados) na pasta selecionada
        file_num_display_elem = sg.Text('File 1 of {}'.format(self.getNumFiles()), size=(15, 1))

        #componente do PySimpleGUI que exibe a imagem(não da pra manipular os dados, pois é um objt do tipo sg.Image)
        image_elem1 = sg.Image(data=self.get_img_data(filename, first=True))
        #elemento do PySimpleGUI que exive o nome do arquivo selecionado
        filename_display_elem1 = sg.Text(filename, size=(80, 1), key='file1')
        
        image_elem2 = sg.Image(data=self.get_img_data(filename, first=True))
        filename_display_elem2 = sg.Text(filename, size=(80, 1), key='file2')

        # exibe o nome do arquivo seleciona e a imagem
        col1 = [[filename_display_elem1],
                [image_elem1]]

        col2 = [[filename_display_elem2],
                [image_elem2]]


        #exibe os nomes dos arquivos e os botões 'next' e 'prev'
        col_files = [[sg.Listbox(values=self.getFileNames(), change_submits=True, size=(30, 30), key='listbox')],
                    [sg.Button('Imagem 1', size=(8, 2)), sg.Button('Imagem 2', size=(8, 2)), file_num_display_elem]]

        #layout da aplicação
        layout = [[sg.Column(col_files), sg.Column(col1), sg.Column(col2)]]

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
            elif event == 'listbox':
                f = values["listbox"][0]                        # filename selecionado
                filename = os.path.join(self.getFolder(), f)    # lê o arquivo selecionado
                i = self.getFileNames().index(f)                # atualiza o index
            else:
                filename = os.path.join(self.getFolder(), self.getFileNames()[i])
            
            if event == 'Imagem 1':
                # atualiza a janela com a nova imagem
                image_elem1.update(data=self.get_img_data(filename, first=True))
                # atualizaz a janela com o novo nome da imagem
                filename_display_elem1.update(filename)
            elif event == 'Imagem 2':
                # atualiza a janela com a nova imagem
                image_elem2.update(data=self.get_img_data(filename, first=True))
                # atualizaz a janela com o novo nome da imagem
                filename_display_elem2.update(filename)

            file_num_display_elem.update('File {} of {}'.format(i+1, self.getNumFiles()))

        window.close()        
screen = Main()
screen.Iniciar()
