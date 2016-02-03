from tkinter import *


class MyMenu:
    """Esta classe cria um menu para a janela principal onde são passadas opções e comandos ao programa: ele poderá
        ser resetado (reset e full-reset), mudar o nível de log, fechar o programa........
    """

    def __init__(self, parent, frame1, frame3):
        self.frame1 = frame1
        self.frame3 = frame3

        # Criando a menubar na janela principal e adicionando os menus
        parent.option_add('*tearOff',  FALSE)
        self.menubar = Menu(parent)
        parent['menu'] = self.menubar

        self.menu_file = Menu(self.menubar)
        self.menu_options = Menu(self.menubar)
        self.menu_help = Menu(self.menubar)

        self.menubar.add_cascade(menu=self.menu_file, label='Arquivo')
        self.menubar.add_cascade(menu=self.menu_options, label='Opções')
        self.menubar.add_cascade(menu=self.menu_help, label='Ajuda')

        self.menu_file.add_command(label='Reset') # implementar o command: , command)
        self.menu_file.add_command(label='Full-Reset') # implementar o command: , command)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Fechar') # implementar o command: , command)

        self.perdeutCheck = IntVar()
        self.perdeutCheck.set(0)
        self.menu_options.add_checkbutton(label='Usar perdeuterado',  variable=self.perdeutCheck,  onvalue=1,
                                          offvalue=0,  command=self.AtualizaPerdeutCheck)
        self.menu_options.add_separator()
        self.menu_log = Menu(self.menu_options)
        self.menu_options.add_cascade(menu=self.menu_log, label='Nível de Log:')
        self.logRadiobutton = IntVar()
        self.logRadiobutton.set(2)
        self.menu_log.add_radiobutton(label='Debug', variable=self.logRadiobutton, value=1)
        self.menu_log.add_radiobutton(label='Info', variable=self.logRadiobutton, value=2)
        self.menu_log.add_radiobutton(label='Warn', variable=self.logRadiobutton, value=3)
        self.menu_log.add_radiobutton(label='Error', variable=self.logRadiobutton, value=4)
        self.menu_log.add_radiobutton(label='Critical', variable=self.logRadiobutton, value=5)

        self.menu_help.add_command(label='Sobre') # implementar o command: , command)

    def AtualizaPerdeutCheck(self):

        self.frame3.AtualizaPerdeutCheck(self.perdeutCheck.get())