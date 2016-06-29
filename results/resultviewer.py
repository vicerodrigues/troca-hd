from tkinter import *
from tkinter import ttk
import os
from menu import frmenu
from log import frlog
from fileIO import importarquivo


class JanelaResultados(Toplevel):
	"""Classe  que inicializa a janela de apresentação dos resultados. Herda de Toplevel.
	"""

	def __init__(self, controller, resultado, r2):

		# Inicializando variáveis locais
		self.controller = controller
		self.resultado = resultado
		self.r2 = r2

		# Inicializando a classe Toplevel de quem JanelaResultados herda
		Toplevel.__init__(self, class_='Trocahd')

		# Definindo título, ícone e posição da janela
		self.title("Resultados")
		img = PhotoImage(file=os.path.expanduser('~/Calculator.png'))
		self.tk.call('wm', 'iconphoto', self._w, img)
		self.geometry('+725+50')

		# Fazendo o bind das teclas de atalho
		self.bind('<Control-q>', self.on_closing_results)
		self.bind('<Control-r>', self.controller.frames[frmenu.MyMenu].resetSoft)
		self.bind('<Control-R>', self.controller.frames[frmenu.MyMenu].fullResetSoft)
		self.bind('<Control-s>', self.controller.frames[frmenu.MyMenu].saveLog)

		# Função executada no fechamento da janela
		self.protocol('WM_DELETE_WINDOW', self.on_closing_results)

		# Frame externo
		self.outerFrame = ttk.Frame(self, relief='ridge', borderwidth=2)
		self.outerFrame.grid(row=0, column=0, sticky=(N, S, E, W), padx=1, pady=1)

		# Frame interno
		self.resultsFrame = ttk.Frame(self.outerFrame, padding=(5, 5, 5, 5), relief=RIDGE, borderwidth=2)
		self.resultsFrame.grid(row=0, column=0, sticky=(N, S, E, W), padx=2, pady=2)

		# Chamada da função que inicializa os widgets
		self.populaJanela()

	def populaJanela(self):
		"""
		"""

		# Label para o titulo do frame
		self.labelJanelaResultados = ttk.Label(self.resultsFrame, text='Resultados:', font='TkCaptionFont')
		self.labelJanelaResultados.grid(row=0, column=0, columnspan=3, sticky=W, pady=(5, 10))

		# Textbox para apresentação dos resultados
		self.resultados = Text(self.resultsFrame, width=12, height=10, wrap='none')
		self.resultados.grid(row=1, column=0, rowspan=5)
		self.resultados.configure(state='disabled')

		# Popula o Textbox com os resultados
		self.resultados.configure(state='normal')
		self.resultados.insert('end', 'Teores:\n')
		for i in range(len(self.resultado)):
			self.resultados.insert('end', 'D%i = %4.1f%%\n' %(i, self.resultado[i]))
		self.resultados.configure(state='disabled')

        # Criando as ScrollBars e associando a TextBox
		self.resultadosdScrollV = ttk.Scrollbar(self.resultsFrame, orient=VERTICAL,
                                                         command=self.resultados.yview)
		self.resultadosdScrollV.grid(row=1, column=1, rowspan=5, sticky=(N, S))
		self.resultados['yscrollcommand'] = self.resultadosdScrollV.set
		self.resultadosdScrollH = ttk.Scrollbar(self.resultsFrame, orient=HORIZONTAL,
                                                         command=self.resultados.xview)
		self.resultadosdScrollH.grid(row=6, column=0, sticky=(E, W))
		self.resultados['xscrollcommand'] = self.resultadosdScrollH.set

		# Criando o frame da direita que conterá os botões e as labels que apresentam parte dos resultados (Phi, R² e MDC)
		self.rightFrame = ttk.Frame(self.resultsFrame)
		self.rightFrame.grid(row=1, column=2, rowspan=6)

		# Calcula Phi e mostra o resultado no label
		self.myPhi = 0
		for i in range(1, len(self.resultado)):
			self.myPhi += i*self.resultado[i]/100
		self.lblPhi = ttk.Label(self.rightFrame, text='Phi = %12.1f' %self.myPhi)
		self.lblPhi.grid(row=1, column=2, sticky=W, padx=(10, 5), pady=(0, 5))

		# Calcula MDC e mostra no label
		self.MDC = self.myPhi/(len(self.resultado)-1)*100
		self.lblMDC = ttk.Label(self.rightFrame, text='MDC(%%) = %.1f' %self.MDC)
		self.lblMDC.grid(row=2, column=2, sticky=W, padx=(10, 5), pady=(5, 5))

		# Mostra R² no label
		self.lblR2 = ttk.Label(self.rightFrame, text='R² = %11.4f' %self.r2)
		self.lblR2.grid(row=3, column=2, sticky=W, padx=(10, 5), pady=(5, 5))

		# Botão para salvar os resultados
		self.btnSalvar = ttk.Button(self.rightFrame, text='Salvar', command=self.salvaResultados)
		self.btnSalvar.grid(row=4, column=2, sticky='ew', padx=(10, 5), pady=(5, 5))
		self.btnSalvar.bind('<Return>', lambda x: self.salvaResultados())

		# Botão para exibir janela com o gráfico - Em andamento
		self.btnGraph = ttk.Button(self.rightFrame, text='Gráfico', command=self.plotarGrafico())
		self.btnGraph.grid(row=5, column=2, sticky='ew', padx=(10, 5), pady=(5, 0))
		self.btnGraph.bind('<Return>', lambda x: self.plotarGrafico())
		self.btnGraph.configure(state='disabled')

		# Move o foco para o botão de salvar os resultados
		self.btnSalvar.focus_force()

	def salvaResultados(self):
		"""Função que salva os resultados em um arquivo excel.
		"""

		self.metodo = self.controller.frames[frmenu.MyMenu].methodRadiobutton.get()
		self.controller.frames[frlog.FrameLog].WriteLog('info', 'Salvando arquivo com os resultados da simulação.')
		importarquivo.IniciaArquivo('Resultsave', controller=self.controller).salvarArquivo(self.resultado, \
					self.myPhi, self.MDC, self.r2, self.metodo)

		# Este foco está comentado pois a função ainda não foi implementada
		#self.btnGraph.focus_force()

	def on_closing_results(self, *args):
		"""Função executada no fechamento da janela.
		"""

		# Fecha a janela e iguala a variável associada a None
		self.controller.results_window.destroy()
		self.controller.results_window = None

	def plotarGrafico(self):
		"""Não implementada.
		"""

		pass

