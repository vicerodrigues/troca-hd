import numpy as np
import scipy.optimize as opt
from menu import frmenu
from log import frlog
import logging
from results import resultviewer


class SimularEspectro:
	"""Classe que realiza a simulação do espectro da mistura e instancia a janela que mostra os resultados.
	"""

	def __init__(self, controller, mistura, massSpectra):

		# Inicialização de variáveis locais
		self.controller = controller
		self.mistura = mistura
		self.massSpectra = massSpectra
		self.simular()

	def simular(self):
		"""Função que realiza a simulação e inicia o módulo resultviewer que é a janela de apresentação dos resultados.
		"""

		# A utilização de numpy e scipy no cálculo das simulações necessita a inicialização das listas como arrays numpy
		self.myY = np.array(self.mistura)
		self.myX = np.array(self.massSpectra)

		# Determina qual o método a ser utilizado na simulação e o aplica 
		if self.controller.frames[frmenu.MyMenu].methodRadiobutton.get() == 1:
			# realiza a simulação
			self.myA, self.resid = np.linalg.lstsq(self.myX, self.myY)[:2]
			# Calcula R²
			self.r2 = 1-self.resid/(self.myY.size*self.myY.var())
			self.metodo = 'Least-squares'
		else:
			# realiza a simulação
			self.myA, self.normResid = opt.nnls(self.myX, self.myY[:,0])
			# Calcula R²
			self.r2 = 1-self.normResid/(np.linalg.norm(self.myY))
			self.metodo = 'Non-negative least-squares'
		# passa o resultado para a respectiva variável
		self.resultado=self.myA/self.myA.sum(axis=0)*100

		# Escreve os resultados no LOG
		self.controller.frames[frlog.FrameLog].WriteLog('info', 'Simulando o espectro da mistura utilizando o método %s'\
					 %self.metodo)

		self.controller.frames[frlog.FrameLog].WriteLog('info', 'Resultado de composição da mistura:')
		self.controller.frames[frlog.FrameLog].text_handler.setFormatter(logging.Formatter('%(message)s'))
		for i in range(len(self.resultado)):
			self.controller.frames[frlog.FrameLog].WriteLog('info', ' '*7 + 'D[%i]: ' %i + '%5.2f%%' %self.resultado[i] + '\n')
		self.controller.frames[frlog.FrameLog].WriteLog('info', '\n' + ' '*7 + 'R^2 : %6.4f' %self.r2 + '\n')
		self.controller.frames[frlog.FrameLog].WriteLog('info', '\n')
		self.controller.frames[frlog.FrameLog].text_handler.setFormatter(logging.Formatter(self.controller.frames[frlog.FrameLog].\
                format_))

		self.controller.frames[frlog.FrameLog].WriteLog('info', 'Abrindo a janela de resultados')

		# Determina se a janela de resultados existe e a recarrega
		if self.controller.results_window:
			self.controller.results_window.destroy()
		
		# Instancia a classe JanelaResultados de resultviewer e a atribui a variável results_window da classe principal
		self.controller.results_window = resultviewer.JanelaResultados(self.controller, self.resultado, self.r2)