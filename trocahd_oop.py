#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
import frmolec
import frlog
import frfiles
import frmenu


# import tkinter.messagebox as messagebox


class TrocaMain(Tk):
    """Classe principal do programa de cálculo para troca H-D.
        Nesta classe é criado o frame principal e são chamadas as classes que criam
        os frames secundários que criam as demais partes do programa.
    """
        
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        # Inicia frame mestre em self
        self.mainFrame = ttk.Frame(self, relief='ridge', borderwidth=2)  # Retirada a opção de relief:
                                                                        # , relief=RAISED, borderwidth=2)
        self.mainFrame.grid(row=0, column=0, sticky=(N, S, E, W), padx=1, pady=1)

        self.frames = {}

        # Frame LOG TextBox
        # global frame1  -  Não foi necessário declarar frame1 como global, somente
        # passar a instancia dele para as outras classes :)
        self.frame1 = frlog.FrameLog(self.mainFrame, self)
        self.frames[frlog.FrameLog] = self.frame1
        self.frame1.grid(row=0, column=1, sticky=(N, S, E, W))

        # Frame Abre Arquivos
        self.frame2 = frfiles.FrameAbreArquivos(self.mainFrame, self, self.frame1)
        self.frames[frfiles.FrameAbreArquivos] = self.frame2
        self.frame2.grid(row=1, column=0, sticky=(N, S, E, W), columnspan=2)

        # Frame Inicia Molecula
        self.frame3 = frmolec.FrameIniciaMolecula(self.mainFrame, self, self.frame1, self.frame2)
        self.frames[frmolec.FrameIniciaMolecula] = self.frame3
        self.frame3.grid(row=0, column=0, sticky=(N, S, E, W))

        # Não é um frame, e por isso não precisa de grid. Popula diretamente a menubar.
        self.frame4 = frmenu.MyMenu(self, self.frame1, self.frame3)
        self.frames[frmenu.MyMenu] = self.frame4
        
        # def on_closing():
        # Criar aqui o docstring
        #    if messagebox.askokcancel('Fechar', 'Gostaria de fechar o programa?'):
        #        inst.destroy()
        # Adicionar nesta função o lembrete das últimas opções utilizadas na corrida

if __name__ == '__main__':
    myTroca = TrocaMain()
    myTroca.title('Troca H-D Calculator')
    img = PhotoImage(file='/home/vicerodrigues/Calculator.png')
    myTroca.tk.call('wm', 'iconphoto', myTroca._w, img)
    myTroca.geometry('+75+50')
    # myTroca.protocol('WM_DELETE_WINDOW', on_closing)
    myTroca.mainloop()
