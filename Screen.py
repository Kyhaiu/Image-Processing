import PySimpleGUI as sg

class Screen:

    def __init__(self, menu, layout, name):
        self.setMenu(menu)
        self.setLayout(layout)
        self.setName(name)
        self.setScreen(name, menu, layout)

    def getScreen(self):
        return self.screen

    def getMenu(self):
        return self.menu

    def getLayout(self):
        return self.layout

    def getName(self):
        return self.name

    def setScreen(self, name, menu, layout):
        sg.theme('DarkBlue1')
        self.screen = sg.Window(name, layout, finalize=True, size=(600, 300))
    
    def setMenu(self, _menu):
        self.menu = _menu

    def setLayout(self, _layout):
        self.layout = _layout

    def setName(self, _name):
        self.name = _name

    def updateLayoutComponents(self, element, newItens):
        self.getScreen().FindElement(element).Update(values=newItens)

    def killWindows(self):
        self.getScreen().Close()
    