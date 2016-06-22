from tkinter import *
from tkinter import ttk
import numpy as np
import scipy.optimize as opt
import os
import frmenu

class SimularEspectro:

	def __init__(self, controller, mistura, massSpectra):

		self.controller = controller
		self.mistura = mistura
		self.massSpectra = massSpectra
		self.simular()

	def simular(self):
		
		self.myY = np.array(self.mistura)
		self.myX = np.array(self.massSpectra)

		if self.controller.frames[frmenu.MyMenu].methodRadiobutton.get() == 1:
			self.myA, self.resid = np.linalg.lstsq(self.myX, self.myY)[:2]
			self.r2 = 1-self.resid/(self.myY.size*self.myY.var())
		else:
			self.myA, self.normResid = opt.nnls(self.myX, self.myY[:,0])
			self.r2 = 1-self.normResid/(np.linalg.norm(self.myY))
		self.resultado=self.myA/self.myA.sum(axis=0)*100

		self.JanelaResultados()

	def JanelaResultados(self):
		
		if self.controller.child_window:
			self.controller.child_window.destroy()
		self.counter = 0
		self.counter += 1
		self.controller.child_window = Toplevel(self.controller, class_='Trocahd')
		self.controller.child_window.title("Resultados")
		img = PhotoImage(file=os.path.expanduser('~/Calculator.png'))
		self.controller.child_window.tk.call('wm', 'iconphoto', self.controller.child_window._w, img)
		self.controller.child_window.geometry('+750+50')
		l = ttk.Label(self.controller.child_window, text="This is window #%s" % self.counter)
		l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    #myTroca = TrocaMain()
    #myTroca.title('Troca H-D Calculator')
    #img = PhotoImage(file=os.path.expanduser('~/Calculator.png'))#file='/home/vicerodrigues/Calculator.png')
    #myTroca.tk.call('wm', 'iconphoto', myTroca._w, img)
    #myTroca.geometry('+75+50')
    #myTroca.mainloop()

