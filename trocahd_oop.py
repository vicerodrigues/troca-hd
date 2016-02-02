#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
import frmolec
import frlog
import frfiles


# import tkinter.messagebox as messagebox


class TrocaMain(Tk):
    """Classe principal do programa de cálculo para troca H-D.
        Nesta classe é criado o frame principal e são chamadas as classes que criam
        os frames secundários que criam as demais partes do programa.
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Inicia frame mestre em self
        self.mainFrame = ttk.Frame(self, relief=RAISED, borderwidth=2)
        self.mainFrame.grid(row=0, column=0, sticky=(N, S, E, W), padx=1, pady=1)

        self.frames = {}

        # Frame LOG TextBox
        # global frame1  -  Não foi necessário declarar frame1 como global, somente
        # passar a instancia dele para as outras classes :)
        frame1 = frlog.FrameLog(self.mainFrame, self)
        self.frames[frlog.FrameLog] = frame1
        frame1.grid(row=0, column=1, sticky=(N, S, E, W))

        # Frame Inicia Molecula
        frame2 = frmolec.FrameIniciaMolecula(self.mainFrame, self, frame1)
        self.frames[frmolec.FrameIniciaMolecula] = frame2
        frame2.grid(row=0, column=0, sticky=(N, S, E, W))

        frame3 = frfiles.FrameAbreArquivos(self.mainFrame, self, frame1)
        self.frames[frfiles.FrameAbreArquivos] = frame3
        frame3.grid(row=1, column=0, sticky=(N, S, E, W), columnspan=2)

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
