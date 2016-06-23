from tkinter import *
from tkinter import ttk
import numpy as np
import scipy.optimize as opt
import os
import frmenu
import importarquivo

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
		
		if self.controller.results_window:
			self.controller.results_window.destroy()

		self.counter = 1

		self.controller.results_window = Toplevel(self.controller, class_='Trocahd')

		self.controller.results_window.title("Resultados")
		img = PhotoImage(file=os.path.expanduser('~/Calculator.png'))
		self.controller.results_window.tk.call('wm', 'iconphoto', self.controller.results_window._w, img)
		self.controller.results_window.geometry('+725+50')
		self.controller.results_window.bind('<Control-q>', lambda x: self.controller.results_window.destroy())

		self.outerFrame = ttk.Frame(self.controller.results_window, relief='ridge', borderwidth=2)
		self.outerFrame.grid(row=0, column=0, sticky=(N, S, E, W), padx=1, pady=1)

		self.resultsFrame = ttk.Frame(self.outerFrame, padding=(5, 5, 5, 5), relief=RIDGE, borderwidth=2)
		self.resultsFrame.grid(row=0, column=0, sticky=(N, S, E, W), padx=2, pady=2)

		self.populaJanela()

	def populaJanela(self):

        # Label para o titulo do frame
		self.labelJanelaResultados = ttk.Label(self.resultsFrame, text='Resultados:', font='TkCaptionFont')
		self.labelJanelaResultados.grid(row=0, column=0, columnspan=3, sticky=W, pady=(5, 10))

		self.resultados = Text(self.resultsFrame, width=12, height=10, wrap='none')
		self.resultados.grid(row=1, column=0, rowspan=5)
		self.resultados.configure(state='disabled')

		# coloca essas linhas em função separada
		self.resultados.configure(state='normal')
		self.resultados.insert('end', 'Teores:\n')
		for i in range(len(self.resultado)):
			self.resultados.insert('end', 'D%i = %4.1f%%\n' %(i, self.resultado[i]))
		self.resultados.configure(state='disabled')

        # Criando a ScrollBar e associando a TextBox
		self.resultadosdScrollV = ttk.Scrollbar(self.resultsFrame, orient=VERTICAL,
                                                         command=self.resultados.yview)
		self.resultadosdScrollV.grid(row=1, column=1, rowspan=5, sticky=(N, S))
		self.resultados['yscrollcommand'] = self.resultadosdScrollV.set
		self.resultadosdScrollH = ttk.Scrollbar(self.resultsFrame, orient=HORIZONTAL,
                                                         command=self.resultados.xview)
		self.resultadosdScrollH.grid(row=6, column=0, sticky=(E, W))
		self.resultados['xscrollcommand'] = self.resultadosdScrollH.set

		self.rightFrame = ttk.Frame(self.resultsFrame)
		self.rightFrame.grid(row=1, column=2, rowspan=6)

		self.myPhi = 0
		for i in range(1, len(self.resultado)):
			self.myPhi += i*self.resultado[i]/100
		self.lblPhi = ttk.Label(self.rightFrame, text='Phi = %12.1f' %self.myPhi)
		self.lblPhi.grid(row=1, column=2, sticky=W, padx=(10, 5), pady=(0, 5))

		self.MDC = self.myPhi/(len(self.resultado)-1)*100

		self.lblMDC = ttk.Label(self.rightFrame, text='MDC(%%) = %.1f' %self.MDC)
		self.lblMDC.grid(row=2, column=2, sticky=W, padx=(10, 5), pady=(5, 5))

		self.lblR2 = ttk.Label(self.rightFrame, text='R^2 = %7.4f' %self.r2)
		self.lblR2.grid(row=3, column=2, sticky=W, padx=(10, 5), pady=(5, 5))

		self.btnSalvar = ttk.Button(self.rightFrame, text='Salvar', command=self.salvaResultados)
		self.btnSalvar.grid(row=4, column=2, sticky='ew', padx=(10, 5), pady=(5, 5))
		self.btnSalvar.bind('<Return>', lambda x: self.salvaResultados())

		self.btnGraph = ttk.Button(self.rightFrame, text='Gráfico', command=self.plotarGrafico())
		self.btnGraph.grid(row=5, column=2, sticky='ew', padx=(10, 5), pady=(5, 0))
		self.btnGraph.bind('<Return>', lambda x: self.plotarGrafico())

		self.btnSalvar.focus_force()

	def salvaResultados(self):

		self.metodo = self.controller.frames[frmenu.MyMenu].methodRadiobutton.get()
		importarquivo.IniciaArquivo('Resultsave').salvarArquivo(self.resultado, self.myPhi, self.MDC, self.r2,\
																 self.metodo)

		self.btnGraph.focus_force()

	def plotarGrafico(self):

		pass
