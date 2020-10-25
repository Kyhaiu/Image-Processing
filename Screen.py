import Image as img
import PySimpleGUI as sg

class Screen:

    def __init__(self):
        
        col1 = [[sg.Text("Imagem 1", pad=((5, 5), (7, 5)))],
                [sg.InputText('Importar Imagem 1', key='folderImg1', disabled=True ,size=(40,1), text_color='black', pad=((5,10),(5,10)), enable_events=True), 
                 sg.FileBrowse(button_text='Procurar', file_types=(("Bmp Files", "*.bmp"),) , tooltip='Realiza a importação da imagem 1', pad=((5,10),(20,10)), key='file1')],
                [sg.Text("Imagem 2")],
                [sg.InputText('Importar Imagem 2', key='folderImg2', disabled=True ,size=(40,1), text_color='black', pad=((5,10),(5,10)), enable_events=True),
                 sg.FileBrowse(button_text='Procurar', file_types=(("Bmp Files", "*.bmp"),) , tooltip='Realiza a importação da imagem 2', pad=((5,10),(20,10)), key='file2')]]

        col2 = [[sg.Text('Operações Aritméticas', size=(17, 1)), sg.Text('Operações Lógicas')],
                [sg.Radio('Adição',        'radioOP', default=True,  key='add', size=(15, 1)), sg.Radio('E lógico',   'radioOP', default=False, key='and')],
                [sg.Radio('Subtração',     'radioOP', default=False, key='sub', size=(15, 1)), sg.Radio('OU lógico',  'radioOP', default=False, key='or' )],
                [sg.Radio('Multiplicação', 'radioOP', default=False, key='mul', size=(15, 1)), sg.Radio('Negação',    'radioOP', default=False, key='not')],
                [sg.Radio('Divisão',       'radioOP', default=False, key='div', size=(15, 1))],
                [sg.SaveAs('Salvar', file_types=(("Bmp Files", "*.bmp"),)), sg.Button('DEGUB COMPONENTS')]]
        
        col3 = [[sg.Text('Imagem resultado', size=(20, 1))], [sg.Image(data=None, size=(320, 320), key='thumbnail')]]
        """
            Componente do PySimpleGUI que exibe a imagem
            sg.Image(data=self.img.generate_thumbnail(filename, first=True)
        """

        aux = [[sg.Column(col1), sg.Column(col2)], [sg.Column(col3)]]

        self.setLayout(aux)
        self.setScreen('name', self.getLayout())
        del aux

    def getScreen(self):
        return self.screen

    def getMenu(self):
        return self.menu

    def getLayout(self):
        return self.layout

    def getName(self):
        return self.name

    def setScreen(self, name, layout):
        sg.theme('DarkBlue1')
        self.screen = sg.Window(name, layout, finalize=True, size=(750, 550))
    
    def setMenu(self, _menu):
        self.menu = _menu

    def setLayout(self, _layout):
        self.layout = _layout

    def setName(self, _name):
        self.name = _name

    def updateLayoutComponents(self, element, _data):
        self.getScreen().FindElement(element).Update(data=_data)

    def killWindows(self):
        self.getScreen().Close()