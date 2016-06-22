from tkinter import *
import frfiles

class MyMenu:
    """Esta classe cria um menu para a janela principal onde são passadas opções e comandos ao programa: ele poderá
        ser resetado (reset e full-reset), mudar o nível de log, fechar o programa........
    """

    def __init__(self, parent, controller):

        self.parent = parent
        self.controller = controller

        # Criando a menubar na janela principal e adicionando os menus
        self.parent.option_add('*tearOff',  FALSE)
        self.menubar = Menu(parent)
        self.parent['menu'] = self.menubar
        
        # Adicionada esta conf para melhorar o visual no Mint que mostrava a menubar alta em relação ao resto
        self.menubar.config(relief='flat')

        self.menu_file = Menu(self.menubar)
        self.menu_options = Menu(self.menubar)
        self.menu_help = Menu(self.menubar)

        self.menubar.add_cascade(menu=self.menu_file, label='Arquivo', underline=0)
        self.menubar.add_cascade(menu=self.menu_options, label='Opções', underline=0)
        self.menubar.add_cascade(menu=self.menu_help, label='Ajuda', underline=1)

        self.menu_file.add_command(label='Reset', accelerator="Ctrl+R", underline=0) # implementar o command: , command)
        self.menu_file.add_command(label='Full-Reset', accelerator="Shift+Ctrl+R", underline=1) # implementar o command: , command)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Fechar', accelerator="Ctrl+Q", underline=0, command = lambda: self.parent.\
            on_closing()) # implementar o command: , command)

        self.perdeutCheck = IntVar()
        self.perdeutCheck.set(0)
        self.menu_options.add_checkbutton(label='Usar perdeuterado',  variable=self.perdeutCheck,  onvalue=1,
                                          offvalue=0,  command=self.AtualizaPerdeutCheck, underline=5)
        #self.menu_options.add_separator()

        self.lembrarCheck = IntVar()
        self.lembrarCheck.set(1)
        self.menu_options.add_checkbutton(label='Lembrar opções',  variable=self.lembrarCheck,  onvalue=1,
                                          offvalue=0, underline=1)#  command=self.AtualizaPerdeutCheck, underline=1)
        self.menu_options.add_separator()

        self.menu_method = Menu(self.menu_options)
        self.menu_options.add_cascade(menu=self.menu_method, label='Método de cálculo:', underline=0)
        self.methodRadiobutton = IntVar()
        self.methodRadiobutton.set(2)
        self.menu_method.add_radiobutton(label='Least-squares', variable=self.methodRadiobutton, value=1, underline=0)
        self.menu_method.add_radiobutton(label='Non-negative least-squares', variable=self.methodRadiobutton, value=2, underline=0)

        self.menu_options.add_separator()

        self.menu_log = Menu(self.menu_options)
        self.menu_options.add_cascade(menu=self.menu_log, label='Nível de Log:', underline=9)
        self.logRadiobutton = IntVar()
        self.logRadiobutton.set(2)
        self.menu_log.add_radiobutton(label='Debug', variable=self.logRadiobutton, value=1, underline=0)
        self.menu_log.add_radiobutton(label='Info', variable=self.logRadiobutton, value=2, underline=0)
        self.menu_log.add_radiobutton(label='Warn', variable=self.logRadiobutton, value=3, underline=0)
        self.menu_log.add_radiobutton(label='Error', variable=self.logRadiobutton, value=4, underline=0)
        self.menu_log.add_radiobutton(label='Critical', variable=self.logRadiobutton, value=5, underline=0)

        self.menu_help.add_command(label='Sobre', underline=0) # implementar o command: , command)

        #Substituir essa função por um trace na variável

    def AtualizaPerdeutCheck(self):

        self.parent.frames[frfiles.FrameAbreArquivos].AtualizaPerdeutCheck()