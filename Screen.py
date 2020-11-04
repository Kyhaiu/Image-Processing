import PySimpleGUI as sg

class Screen:

    def __init__(self):
        
        frame1_layout = [
                            [sg.Input(key='-FILEBROWSE1-', enable_events=True, visible=False), sg.Image(data=None, size=(320, 320), key='thumbnail_image_1')],
                            [sg.Text(text='', key='-SIZE-IMG1-', size=(11, 1)),
                             sg.Text(text='', key='-BIT-DEPTH-IMG1-', size=(6, 1))],
                            [sg.FileBrowse(button_text='Abrir Imagem', target='-FILEBROWSE1-', file_types=(("Bmp Files", "*.bmp"),) , tooltip='Realiza a importação da imagem 1 com formato .bmp e resolução de cores de 1-bit, 8-bits, 24-bits'),
                             sg.Checkbox('Not', default=False, key='-NOT-IMG1-', enable_events=True, tooltip='Aplica a operação lógica NOT na imagem 1')]
                        ]

        frame2_layout = [
                            [sg.Input(key='-FILEBROWSE2-', enable_events=True, visible=False), sg.Image(data=None, size=(320, 320), key='thumbnail_image_2')],
                            [sg.Text(text='', key='-SIZE-IMG2-', size=(11, 1)),
                             sg.Text(text='', key='-BIT-DEPTH-IMG2-', size=(6, 1))],
                            [sg.FileBrowse(button_text='Abrir Imagem', target='-FILEBROWSE2-', file_types=(("Bmp Files", "*.bmp"),) , tooltip='Realiza a importação da imagem 2 com formato .bmp e resolução de cores de 1-bit, 8-bits, 24-bits'),
                             sg.Checkbox('Not', default=False, key='-NOT-IMG2-', enable_events=True, tooltip='Aplica a operação lógica NOT na imagem 1')]
                        ]
        frame3_logical_operation_layout = [
                                            [sg.Radio('E lógico',   'radioOP', default=False, key='-AND-', tooltip='Operação logíca que compara bit-a-bit, e retorna verdadeiro quando os dois bits comparados tem valores lógicos igual a 1 \n Ex.:  --------------------------\n        | Bit 1 | Bit 2 | Bit 1 E Bit 2 | \n        | ----  | ----  | -----------  | \n        |    0    |    0    |         0          | \n        |    0    |    1    |         0          | \n        |    1    |    0    |         0          | \n        |    1    |    1    |         1          | \n         --------------------------')],
                                            [sg.Radio('OU lógico',  'radioOP', default=False, key='-OR-',  tooltip='Operação lógica que compara bit-a-bit, e retorna verdadeiro quando um ou mais bits comparados tem valor(es) lógico(s) igual a 1 \n Ex.:  ----------------------------\n        | Bit 1 | Bit 2 | Bit 1 OU Bit 2 | \n        | ----  | ----  | -------------- | \n        |    0    |    0    |           0           | \n        |    0    |    1    |           1           | \n        |    1    |    0    |           1           | \n        |    1    |    1    |           1           | \n         ----------------------------')],
                                            [sg.Radio('XOR lógico', 'radioOP', default=False, key='-XOR-', tooltip='Operação lógica que compara bit-a-bit, e retorna verdadeiro quando houver diferença entre os dois bits comparados \n Ex.:  -----------------------------\n        | Bit 1 | Bit 2 | Bit 1 XOR Bit 2 | \n        | ----  | ----  | --------------- | \n        |    0    |    0    |            0            | \n        |    0    |    1    |            1            | \n        |    1    |    0    |            1            | \n        |    1    |    1    |            0            | \n         -----------------------------')],
                                            [sg.Radio('Negação',    'radioOP', default=False, key='-NOT-', tooltip='Operação lógica que inverte os bit(s) de uma imagem \n Ex.:  -------------------\n        | Bit 1 | NOT(Bit 1) | \n        | ----  | -----------  | \n        |    0    |         1          | \n        |    1    |         0          | \n         -------------------')]
                                          ]

        frame3_arithmetic_operation_layout = [
                                                [sg.Radio('Adição',        'radioOP', default=True,  key='-ADD-', size=(15, 1), tooltip='Operação Aritimética que soma a cor de dois pixeis, e retorna a soma normalizada \nutilizando uma operação de auto-escala para o intervalo [0, ... , 255] \nEx.: pixel 1 => R1=42, G1=42, B1=42       + R1, G1, B1\n       pixel 2 => R2=58, G2=58, B2=58          R2, G2, B2 \n                                                                       ____________ \n                                                                        100, 100, 100 \n Obs.: Ri, Gi, Bi equivalem a intensidade de Vermelho, Verde e Azul de cada pixel. \n           E após a soma de todos os pixeis. Os canais são submetidos a uma operação \n           de auto-escala, pois pode haver valores que ultrapassem 255.')],
                                                [sg.Radio('Subtração',     'radioOP', default=False, key='-SUB-', size=(15, 1), tooltip='Operação Aritimética que subtrai a cor de dois pixeis, e retorna a subtração normalizada \nutilizando uma operação de auto-escala para o intervalo [0, ... , 255] \nEx.: pixel 1 => R1=42, G1=42, B1=42       - R1, G1, B1\n       pixel 2 => R2=58, G2=58, B2=58          R2, G2, B2 \n                                                                       ____________ \n                                                                        -16, -16, -16 \n Obs.: Ri, Gi, Bi equivalem a intensidade de Vermelho, Verde e Azul de cada pixel. \n           E após a subtração de todos os pixeis. Os canais são submetidos a uma operação \n           de auto-escala, pois podem haver valores que sejam negativos causando assim \n           um underflow.')],
                                                [sg.Radio('Multiplicação', 'radioOP', default=False, key='-MUL-', size=(15, 1), tooltip='Operação Aritimética que multiplica a cor de dois píxeis, e retorna a multiplicação normalizada \nutilizando uma operação de auto-escala para o intervalo [0, ..., 255] \nEx.: pixel 1 => R1=42, G1=42, B1=42       * R1, G1, B1\n       pixel 2 => R2=58, G2=58, B2=58          R2, G2, B2 \n                                                                       ____________ \n                                                                        2436, 2436, 2436 \n Obs.: Ri, Gi, Bi equivalem a intensidade de Vermelho, Verde e Azul de cada pixel. \n           E após a multiplicação de todos os pixeis. Os canais são submetidos a uma operação \n           de auto-escala, pois pode haver valores que sejam maiores que 255 causando assim \n           um overflow.')],
                                                [sg.Radio('Divisão',       'radioOP', default=False, key='-DIV-', size=(15, 1), tooltip='Operação Aritimética que divide a cor de dois píxeis, e retorna a divisão normalizada \nutilizando uma operação de auto-escala para o intervalo [0, ..., 255] \nEx.: pixel 1 => R1=42, G1=42, B1=42       * R1, G1, B1\n       pixel 2 => R2=58, G2=58, B2=58          R2, G2, B2 \n                                                                       ____________ \n                                                                        0.724, 0.724, 0.724 \n Obs.: Ri, Gi, Bi equivalem a intensidade de Vermelho, Verde e Azul de cada pixel. \n           E após a divisão de todos os pixeis. Os canais são submetidos a uma operação \n           de auto-escala, pois pode haver valores em ponto flutuante, e para solucionar \n           este problema pega-se somente a parte inteira.')]
                                             ]
        frame3_layout = [
                            [sg.Frame('Aritiméticas', frame3_arithmetic_operation_layout), sg.Frame('Lógicas', frame3_logical_operation_layout)],
                            [sg.Input(key='-FILESAVE-', enable_events=True, visible=False), 
                             sg.Button('Aplicar operação', key='-APPLYOP-', tooltip=' Botão que aplica a operação selecionada nas imagem 1 e imagem 2\n Obs.:A operação Negação é a excessão pois ela executa em cima de um resultado prévio'),
                             sg.FileSaveAs('Salvar Imagem', file_types=(("Bmp Files", "*.bmp"),), key='-SAVE-', target='-FILESAVE-', disabled=True, tooltip=' Botão que salva a imagem resultado com formato bmp.\n Obs.: Como a imagem é salva como bmp é necessário colocar a extenssão correta "imagem - Resultado.bmp"')],
                            [sg.T(' ', font=('Helvetica', 1), size=(320, 89))]
                        ]
        frame4_layout = [
                            [sg.Image(data=None, size=(320, 320), key='thumbnail_image_result')],
                            [
                                sg.Text(text='', key='-SIZE-IMG-RESULT-', size=(11, 1)),
                                sg.Text(text='', key='-BIT-DEPTH-RESULT-', size=(6, 1))
                            ]
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
        self.screen = sg.Window(name, layout, finalize=True)
    
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