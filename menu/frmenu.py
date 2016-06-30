from tkinter import *
from tkinter import filedialog
from files import frfiles
from log import frlog
from molecula import frmolec
import os


class MyMenu(Menu):
    """Esta classe cria um menu para a janela principal onde são passadas opções e comandos ao programa: ele poderá
        ser resetado (reset e full-reset), mudar o nível de log, fechar o programa...
    """

    def __init__(self, parent, controller):

        # Inicialização de Menu de quem a classe herda
        Menu.__init__(self, parent)

        # passa as variáveis de pai e controlador
        self.parent = parent
        self.controller = controller

        # Criando a menubar na janela principal e adicionando os menus
        self.parent.option_add('*tearOff',  FALSE) # tearOff FALSE tira o pontilhado do topo do menu
        self.menubar = self # Como herda de Menu, ele própio (self) é o menubar. self.menubar é por legibilidade
        self.parent['menu'] = self.menubar
        
        # Adicionada esta conf para melhorar o visual no Mint que mostrava a menubar alta em relação ao resto
        #self.menubar.config(relief='flat')

        # Criando os três menus disponíveis
        self.menu_file = Menu(self.menubar)
        self.menu_options = Menu(self.menubar)
        self.menu_help = Menu(self.menubar)

        # Adicionando a entrada
        self.menubar.add_cascade(menu=self.menu_file, label='Arquivo', underline=0)
        self.menubar.add_cascade(menu=self.menu_options, label='Opções', underline=0)
        self.menubar.add_cascade(menu=self.menu_help, label='Ajuda', underline=1)

        # Adicionando comandos ao menu Arquivo
        self.menu_file.add_command(label='Reset', accelerator="Ctrl+R", underline=0, command=self.resetSoft)
        self.menu_file.add_command(label='Full-Reset', accelerator="Ctrl+Shift+R", underline=1, command=\
                self.fullResetSoft)

        self.menu_file.add_separator() # Separador para melhorar a visualização
        
        # Adicionando comando para salvar o LOG
        self.menu_file.add_command(label='Salvar Log', accelerator="Ctrl+s", underline=0, command=self.saveLog)
        
        self.menu_file.add_separator() # Separador para melhorar a visualização
        
        self.menu_file.add_command(label='Fechar', accelerator="Ctrl+Q", underline=0, command = lambda: self.parent.\
            on_closing())

        # Populando o menu Opções

        # IntVar responsável pela variável perdeutCheck
        self.perdeutCheck = IntVar()
        #self.perdeutCheck.set(0)
        self.perdeutCheck.set(self.parent.myVars["perdeutCheck"])
        # Checkbutton para determinar se será utilizado o espectro perdeuterado
        self.menu_options.add_checkbutton(label='Usar perdeuterado',  variable=self.perdeutCheck,  onvalue=1,
                                          offvalue=0, underline=5)
        # Trace na variável para verificar mudanças
        self.perdeutCheck.trace('w', self.AtualizaPerdeutCheck)

        # IntVar responsável pela variável lembrarCheck
        self.lembrarCheck = IntVar()
        #self.lembrarCheck.set(1)
        self.lembrarCheck.set(self.parent.myVars["lembrarCheck"])
        # Checkbutton para determinar se as opções serão reutilizadas após a inicialização
        self.menu_options.add_checkbutton(label='Lembrar opções',  variable=self.lembrarCheck,  onvalue=1,
                                          offvalue=0, underline=1)

        # Separador melhora a legibilidade
        self.menu_options.add_separator()
        
        # Comando para resetar opções
        self.menu_options.add_command(label='Resetar opções', underline=0, command=self.resetOptions)

        # Separador melhora a legibilidade
        self.menu_options.add_separator()

        # Criando o sub-menu método onde serão colocadas as opções de métodos numéricos
        self.menu_method = Menu(self.menu_options)
        self.menu_options.add_cascade(menu=self.menu_method, label='Método de cálculo:', underline=0)
        # IntVar responsável pela variável methodRadiobutton
        self.methodRadiobutton = IntVar()
        #self.methodRadiobutton.set(2)
        self.methodRadiobutton.set(self.parent.myVars["methodRadiobutton"])
        # Opções do radiobutton método
        self.menu_method.add_radiobutton(label='Least-squares', variable=self.methodRadiobutton, value=1, underline=0)
        self.menu_method.add_radiobutton(label='Non-negative least-squares', variable=self.methodRadiobutton, value=2, underline=0)
        # Trace que verifica a atualização da variável e recalcular resultados com base no novo método
        self.methodRadiobutton.trace('w', self.mudaMetodo)

        # Separador melhora a legibilidade
        self.menu_options.add_separator()

        # Sub-menu de opções de nível de log do sistema
        self.menu_log = Menu(self.menu_options)
        self.menu_options.add_cascade(menu=self.menu_log, label='Nível de Log:', underline=9)

        # Usa uma StringVar para passar direto o valor esperado pelo Frame de Log
        self.logRadiobutton = StringVar()
        #self.logRadiobutton.set('INFO')
        self.logRadiobutton.set(self.parent.myVars["logRadiobutton"])
        # Adicionando as opções de nível de log
        self.menu_log.add_radiobutton(label='Debug', variable=self.logRadiobutton, value='DEBUG', underline=0)
        self.menu_log.add_radiobutton(label='Info', variable=self.logRadiobutton, value='INFO', underline=0)
        self.menu_log.add_radiobutton(label='Warn', variable=self.logRadiobutton, value='WARN', underline=0)
        self.menu_log.add_radiobutton(label='Error', variable=self.logRadiobutton, value='ERROR', underline=0)
        self.menu_log.add_radiobutton(label='Critical', variable=self.logRadiobutton, value='CRITICAL', underline=0)
        # Trace na variável para atualizar o nível de log
        self.logRadiobutton.trace('w', self.changeLogLevel)

        # Entrada do menu sobre ainda a ser implementada
        self.menu_help.add_command(label='Sobre', underline=0) # implementar o command: , command)

    def AtualizaPerdeutCheck(self, *args):
        """Função do trace da variável que toma conta da lógica de disponibilidade dos widgets do espectro
            perdeuterado
        """

        if self.perdeutCheck.get() == 1:
            self.text = 'Usar espectro perdeuterado.'
        else:
            self.text = 'Não usar espectro perdeuterado'
        
        # Escreve no log a mudança
        self.parent.frames[frlog.FrameLog].WriteLog('info', 'Diretriz de uso do espectro do composto perdeuterado\
 atualizada: ' + self.text)

        if self.parent.results_window != None:
            self.parent.results_window.destroy()
        self.parent.frames[frfiles.FrameAbreArquivos].AtualizaPerdeutCheck()

    def mudaMetodo(self, *args):
        """Função do trace da variável que toma conta da lógica de mudança do método de cálculo do sistema,
            recalculando-o automaticamente quando necessário.
        """

        if self.methodRadiobutton.get() == 1:
            self.text = 'Least-squares.'
        else:
            self.text = 'Non-negative least-squares.'
        
        # Escreve no log a mudança
        self.parent.frames[frlog.FrameLog].WriteLog('info', 'Método de simulação atualizado. Novo método: ' + self.text)

        if self.parent.results_window != None:
            self.parent.frames[frfiles.FrameAbreArquivos].simularEspectros()

    def changeLogLevel(self, *args):
        """Função de trace da variável que muda o nível de log do sistema.
        """

        # Escreve no log o evento
        self.parent.frames[frlog.FrameLog].WriteLog('info', 'Mudança no nível de log do sistema. Novo nível: '\
         + self.logRadiobutton.get())

        self.parent.frames[frlog.FrameLog].logger.setLevel(self.logRadiobutton.get())

    def resetSoft(self, *args):
        """O soft reset simplesmente fecha a janela de resultados e apaga o espectro da mistura previamente carregado
            no programa.
        """
        if self.parent.results_window != None:
            self.parent.results_window.destroy()

        self.parent.frames[frfiles.FrameAbreArquivos].espectroMistura.configure(state='normal')
        self.parent.frames[frfiles.FrameAbreArquivos].espectroMistura.delete(1.0, END)
        self.parent.frames[frfiles.FrameAbreArquivos].espectroMistura.configure(state='disabled')
        self.parent.frames[frfiles.FrameAbreArquivos].checkTratarEspectros()
        self.parent.frames[frfiles.FrameAbreArquivos].btnAbreMistura.focus_force()

        # Escreve no log o evento
        self.parent.frames[frlog.FrameLog].WriteLog('info', 'Executado o Reset do programa.')

    def fullResetSoft(self, *args):
        """O full reset executa um soft reset e em seguida apaga o resto dos espectros já carregados retornando o acesso
            ao frame de iniciar a molécula.
        """
        self.resetSoft()

        # Apagando espectro perdeuterado caso tenha sido aberto
        if self.perdeutCheck.get() == 1:
            self.parent.frames[frfiles.FrameAbreArquivos].espectroPerdeuterado.configure(state='normal')
            self.parent.frames[frfiles.FrameAbreArquivos].espectroPerdeuterado.delete(1.0, END)
            self.parent.frames[frfiles.FrameAbreArquivos].espectroPerdeuterado.configure(state='disabled')

        # Apagando espectro peridrogenado
        self.parent.frames[frfiles.FrameAbreArquivos].espectroPeridrogenado.configure(state='normal')
        self.parent.frames[frfiles.FrameAbreArquivos].espectroPeridrogenado.delete(1.0, END)
        self.parent.frames[frfiles.FrameAbreArquivos].espectroPeridrogenado.configure(state='disabled')

        # desabilitando os botões
        self.parent.frames[frfiles.FrameAbreArquivos].btnAbrePeridrogenado.configure(state='disabled')
        self.parent.frames[frfiles.FrameAbreArquivos].btnAbreMistura.configure(state='disabled')
        self.parent.frames[frfiles.FrameAbreArquivos].btnAbrePerdeuterado.configure(state='disabled')

        # Reabilitando o frame de descrição da molécula
        self.parent.frames[frmolec.FrameIniciaMolecula].carbonNumber.configure(state='normal')
        self.parent.frames[frmolec.FrameIniciaMolecula].hydNumber.configure(state='normal')
        self.parent.frames[frmolec.FrameIniciaMolecula].specMin.configure(state='normal')
        self.parent.frames[frmolec.FrameIniciaMolecula].specMax.configure(state='normal')

        # Reiniciando o FrameIniciaMolecula
        self.parent.frames[frmolec.FrameIniciaMolecula].acceptedMolec = False

        # Movendo o foco para o botão de aceitar a molécula
        self.parent.frames[frmolec.FrameIniciaMolecula].btnAceitar.focus_force()

        # Escreve no log o evento
        self.parent.frames[frlog.FrameLog].WriteLog('info', 'Executado o Full-Reset do programa.')

    def resetOptions(self, *args):
        """Função que devolve todas as opções do programa aos seus parâmetros default (cálculo do benzeno).
        """

        self.parent.frames[frmolec.FrameIniciaMolecula].myCarbonNumber.set(6)
        self.parent.frames[frmolec.FrameIniciaMolecula].myHydNumber.set(6)
        self.parent.frames[frmolec.FrameIniciaMolecula].mySpecMax.set(86)
        self.parent.frames[frmolec.FrameIniciaMolecula].mySpecMin.set(73)

        # (MYSOFTPATH será substituído pelo aplicativo de instalação)
        self.mySoftPath = 'MYSOFTPATH'
        self.myExamplePath = 'examples/'
        # Criação do caminho do diretório examples
        self.parent.openFileDir = os.path.join(self.mySoftPath, self.myExamplePath)
        self.parent.saveFileDir = os.path.join(self.mySoftPath, self.myExamplePath)

        self.perdeutCheck.set(0)
        self.lembrarCheck.set(1)
        self.methodRadiobutton.set(2)        
        self.logRadiobutton.set('INFO')

        # Full reset ao final pois fecha a janela de resultados que é novamente aberta pela mudança do método
        self.fullResetSoft()

        # Escreve no log o evento
        self.parent.frames[frlog.FrameLog].WriteLog('info', 'Reiniciando os parâmetros do programa para seus valores padrão.')

    def saveLog(self, *args):
        """Função que executa o salvamento em arquivo (texto) do Textbox do Log do programa.
        """

        # Opções da caixa de diálogo
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('Text file', '.txt'), ('All files', '.*')]
        options['initialdir'] = os.path.expanduser(self.parent.saveFileDir)
        options['title'] = 'Salvar arquivo de Log'
        options['initialfile'] = 'LogFile.txt'
        
        # Abre arquivo e passa para self.filename
        self.filename = filedialog.asksaveasfilename(**self.file_opt)


        # Função if que identifica se algum arquivo foi escolhido
        if self.filename != '':
            # Faz o update da variável que contém o último diretório de salvamento aberto
            self.parent.saveFileDir = os.path.dirname(self.filename)
            # Abre o arquivo em modo de escrita
            self.file = open(self.filename, 'w')
            # Iterando sobre as linhas do Textbox
            for line in self.parent.frames[frlog.FrameLog].logText.get(1.0, END).splitlines():
                # Escrevendo cada uma das linhas em arquivo
                self.file.writelines(line + '\n')
            # Fecha o arquivo
            self.file.close()
