#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from molecula import frmolec
from log import frlog
from files import frfiles
from menu import frmenu
import tkinter.messagebox as messagebox
import os,pickle


class TrocaMain(Tk):
    """Classe principal do programa de cálculo para troca H-D.
        Nesta classe é criado o frame principal e são chamadas as classes que criam
        os frames secundários responsáveis pelas demais partes do programa.
    """
        
    def __init__(self, *args, **kwargs):

        #Inicializa a classe Tk de onde TrocaMain herda
        Tk.__init__(self, *args, **kwargs)

        # Objeto janela de resultados - Ligado a lógica do programa que regula seu fechamento
        self.results_window = None

        # Função de inicialização responsável pela
        self.on_load()

        # Inicia frame mestre em self (MyTroca que é uma instância de TrocaMain) que conterá todo o resto
        self.mainFrame = ttk.Frame(self, relief='ridge', borderwidth=2)
        self.mainFrame.grid(row=0, column=0, sticky=(N, S, E, W), padx=1, pady=1)

        # Inicia um dicionário vazio que conterá os frames de cada parte do programa
        self.frames = {}

        # Frame LOG TextBox
        # global frame1  -  Não foi necessário declarar frame1 como global, somente
        # passar a instancia dele para as outras classes :)
        self.frames[frlog.FrameLog] = frlog.FrameLog(self.mainFrame)
        self.frames[frlog.FrameLog].grid(row=0, column=1, sticky=(N, S, E, W))

        # Frame Abre Arquivos
        self.frames[frfiles.FrameAbreArquivos] = frfiles.FrameAbreArquivos(self.mainFrame, self)
        self.frames[frfiles.FrameAbreArquivos].grid(row=1, column=0, sticky=(N, S, E, W), columnspan=2)

        # Frame Inicia Molecula
        self.frames[frmolec.FrameIniciaMolecula] = frmolec.FrameIniciaMolecula(self.mainFrame, self)
        self.frames[frmolec.FrameIniciaMolecula].grid(row=0, column=0, sticky=(N, S, E, W))

        # Não é um frame, e por isso não precisa de grid. Popula diretamente a menubar.
        self.frames[frmenu.MyMenu] = frmenu.MyMenu(self, self.mainFrame)

        # Chama a função on_closing ao fechar o aplicativo        
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        # Série de binds de teclas de atalho para funções
        self.bind('<Control-q>', self.on_closing)
        self.bind('<Control-r>', self.frames[frmenu.MyMenu].resetSoft)
        self.bind('<Control-R>', self.frames[frmenu.MyMenu].fullResetSoft)
        self.bind('<Control-s>', self.frames[frmenu.MyMenu].saveLog)

    def on_load(self):
        """Função executada no carregamento do programa que retorna as variáveis guardadas em store.pckl
        """

        # abre o arquivo store.pckl em modo binário de leitura (MYSOFTPATH será substituído pelo aplicativo de instalação)
        self.mySoftPath = 'MYSOFTPATH'
        self.myDataPath = 'data/store.pckl'
        self.file = open(os.path.expanduser(os.path.join(self.mySoftPath, self.myDataPath)), 'rb')
        # utitliza o módulo pickle para recurperar o dicionário guardado
        self.myVars = pickle.load(self.file)
        # fecha o arquivo.
        self.file.close()
        # passa valores para variáveis locais - atualizar diretamente self.myVars não está funcionando
        self.openFileDir = self.myVars["openFileDir"]
        self.saveFileDir = self.myVars["saveFileDir"]

    def on_closing(self, *args):
        """Função acionada no fechamento do programa. Atualiza as novas opções escolhidas na última corrida
            no arquivo store.pckl e checa se o usuário tem certeza que quer sair.
        """

        # Checa se a opção de lembrar está ativada
        if self.frames[frmenu.MyMenu].lembrarCheck.get() == 1:
            # Cria um dicionário vazio onde serão carregadas as opções
            self.myVars = {}
            # popula o dicionário com as opções do programa a serem lembradas
            self.myVars["nCarbon"] = self.frames[frmolec.FrameIniciaMolecula].myCarbonNumber.get()
            self.myVars["nHydrogen"] = self.frames[frmolec.FrameIniciaMolecula].myHydNumber.get()
            self.myVars["specMin"] = self.frames[frmolec.FrameIniciaMolecula].mySpecMin.get()
            self.myVars["specMax"] = self.frames[frmolec.FrameIniciaMolecula].mySpecMax.get()
            self.myVars["openFileDir"] = self.openFileDir
            self.myVars["saveFileDir"] = self.saveFileDir

            self.myVars["perdeutCheck"] = self.frames[frmenu.MyMenu].perdeutCheck.get()
            self.myVars["lembrarCheck"] = self.frames[frmenu.MyMenu].lembrarCheck.get()
            self.myVars["methodRadiobutton"] = self.frames[frmenu.MyMenu].methodRadiobutton.get()
            self.myVars["logRadiobutton"] = self.frames[frmenu.MyMenu].logRadiobutton.get()

            # abre o arquivo store.pckl em modo binário de escrita (MYSOFTPATH será substituído pelo aplicativo de instalação)
            self.mySoftPath = 'MYSOFTPATH'
            self.myDataPath = 'data/store.pckl'
            self.file = open(os.path.expanduser(os.path.join(self.mySoftPath, self.myDataPath)), 'wb')
            # utiliza o módulo pickle para salvar o dicionário
            pickle.dump(self.myVars, self.file)
            # fecha o arqquivo
            self.file.close()
        # chama a message box de saída do programa
        #if messagebox.askokcancel('Fechar', 'Gostaria de fechar o programa?'):
        #    self.destroy()
        self.destroy()

if __name__ == '__main__':
    # Instancia TrocaMain e atribui o classname Trocahd que será utilizado pelo SO para classificar a janela
    myTroca = TrocaMain(className='Trocahd')
    # Título do programa
    myTroca.title('Troca H-D Calculator')
    # Define o ícone do programa (MYSOFTPATH será substituído pelo aplicativo de instalação)
    mySoftPath = 'MYSOFTPATH'
    myDataPath = 'Calculator.png'
    img = PhotoImage(file=os.path.expanduser(os.path.join(mySoftPath, myDataPath)))
    myTroca.tk.call('wm', 'iconphoto', myTroca._w, img)
    # define aonde o programa será aberto
    myTroca.geometry('+75+50')
    # Inicia o loop de execução
    myTroca.mainloop()
