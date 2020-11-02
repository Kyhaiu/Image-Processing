import PySimpleGUI as sg

class Screen:

    def __init__(self):
        
        frame1_layout = [
                            [sg.Input(key='-FILEBROWSE1-', enable_events=True, visible=False), sg.Image(data=None, size=(320, 320), key='thumbnail_image_1')],
                            [sg.FileBrowse(button_text='Abrir Imagem', target='-FILEBROWSE1-', file_types=(("Bmp Files", "*.bmp"),) , tooltip='Realiza a importação da imagem 1'),
                             sg.Checkbox('Not', default=False, key='-NOT-IMG1-', enable_events=True, pad=((190, 0), (0, 0)))]
                        ]

        frame2_layout = [
                            [sg.Input(key='-FILEBROWSE2-', enable_events=True, visible=False), sg.Image(data=None, size=(320, 320), key='thumbnail_image_2')],
                            [sg.FileBrowse(button_text='Abrir Imagem', target='-FILEBROWSE2-', file_types=(("Bmp Files", "*.bmp"),) , tooltip='Realiza a importação da imagem 2'),
                             sg.Checkbox('Not', default=False, key='-NOT-IMG2-', enable_events=True, pad=((178, 0), (0, 0)))]
                        ]
        frame3_logical_operation_layout = [
                                            [sg.Radio('E lógico',   'radioOP', default=False, key='-AND-')],
                                            [sg.Radio('OU lógico',  'radioOP', default=False, key='-OR-' )],
                                            [sg.Radio('XOR lógico', 'radioOP', default=False, key='-XOR-')],
                                            [sg.Radio('Negação',    'radioOP', default=False, key='-NOT-')]
                                          ]
        frame3_arithmetic_operation_layout = [
                                                [sg.Radio('Adição',        'radioOP', default=True,  key='-ADD-', size=(15, 1))],
                                                [sg.Radio('Subtração',     'radioOP', default=False, key='-SUB-', size=(15, 1))],
                                                [sg.Radio('Multiplicação', 'radioOP', default=False, key='-MUL-', size=(15, 1))],
                                                [sg.Radio('Divisão',       'radioOP', default=False, key='-DIV-', size=(15, 1))]
                                             ]
        frame3_layout = [
                            [sg.Frame('Aritiméticas', frame3_arithmetic_operation_layout), sg.Frame('Lógicas', frame3_logical_operation_layout)],
                            [sg.Input(key='-FILESAVE-', enable_events=True, visible=False), 
                             sg.Button('Aplicar operação', key='-APPLYOP-'), sg.FileSaveAs('Salvar Imagem', file_types=(("Bmp Files", "*.bmp"),), key='-SAVE-', target='-FILESAVE-')]
                        ]
        frame4_layout = [
                            [sg.Image(data=None, size=(320, 320), key='thumbnail_image_result')]
                        ]
        
        layout = [
                    [sg.Frame('Imagem 1', frame1_layout),          sg.Frame('Imagem 2',  frame2_layout)],
                    [sg.Frame('Operações', frame3_layout, size=(320, 320)), sg.Frame('Resultado', frame4_layout)]
                 ]
        #aux = [[sg.Column(col1), sg.Column(col2)], [sg.Column(col3)]]

        self.setLayout(layout)
        self.setScreen('PHOTOSHOP PRO PLUSULTRA', self.getLayout())
        del frame1_layout, frame2_layout, frame3_layout, frame4_layout, layout

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
        self.screen = sg.Window(name, layout, finalize=True, size=(700, 750))
    
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