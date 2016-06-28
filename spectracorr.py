import frmolec
import numpy as np

class SpectraCorr:
	"""Módulo que faz as correções da contribuição de 13C nos espectros de massas.
	"""

	def __init__(self, controller, array):

		# Inicializa as variáveis como locais.
		self.controller = controller
		# Array a ser corrigido
		self.array = array

		self.MMD = self.controller.frames[frmolec.FrameIniciaMolecula].myMMD.get()
		self.nMin = self.controller.frames[frmolec.FrameIniciaMolecula].mySpecMin.get()
		self.C13Matrix = self.controller.frames[frmolec.FrameIniciaMolecula].myC13Matrix

	def correctSpec(self):
		"""Função que de fato corrige os espectros.
		"""

		# Itera sobre todas a faixa do espectro.
		for i in range(self.MMD-self.nMin+1):
			# Corrige um valor inicial pelos 13C's perdidos dando o valor absoluto do pico em 12C
			self.array[i] = np.divide(self.array[i],np.array(self.C13Matrix[0]))
			# Para cada um dos possíveis números de 13C corrige as massas seguintes no espectro
			for j in range(1, len(self.C13Matrix)):
				# Pára caso extrapole a faixa do espectro de massas considerada
				if (i+j) >= len(self.array):
					break
				# Correção
				self.array[i+j] = self.array[i+j] - self.C13Matrix[j]*self.array[i]
		# Retorna o array corrigido
		return self.array
