from molecula import frmolec
from aux import combin


class DeuteratedSpectra:
	"""Esta classe cria a matriz dos espectros de massas dos diferentes compostos deuterados a partir de primeiros 
		princípios.
	"""

	def __init__(self, controller, peridrogenado, fatoreshd):
		
		# Inicialização de variáveis locais
		self.controller = controller
		self.peridrogenado = peridrogenado
		self.fatoreshd = fatoreshd

		self.nPoints = self.controller.frames[frmolec.FrameIniciaMolecula].nPoints.get()
		self.nHydrogen = self.controller.frames[frmolec.FrameIniciaMolecula].myHydNumber.get()
		self.nCarbon = self.controller.frames[frmolec.FrameIniciaMolecula].myCarbonNumber.get()
		self.nMin = self.controller.frames[frmolec.FrameIniciaMolecula].mySpecMin.get()
		self.nMax = self.controller.frames[frmolec.FrameIniciaMolecula].mySpecMax.get()
		self.MMH = self.controller.frames[frmolec.FrameIniciaMolecula].myMMH.get()

	def CalcSpec(self):
		"""Função que de fato calcula o espectro de massas dos compostos por primeiros princípios
		"""
		
		# determinando o tamanho da matriz de espectros de massas
		self.rows, self.columns = self.nPoints, (self.nHydrogen+1)

		# Inicializando a matriz com zeros - evita NaN onde não houverem correções
		self.massSpectra = [[0 for column in range(self.columns)] for row in range(self.rows)]

		# Copia o espectro peridrogenado para a primeira coluna
		for i in range(self.nPoints):
			self.massSpectra[i][0] = self.peridrogenado[i]

		# Itera desde 1 átomo de D na molécula até o máximo
		for DinMolec in range(1, self.nHydrogen+1):
			# Número de H's na molécula
			HinMolec = self.nHydrogen - DinMolec
			# Calcula a massa do hidrocarboneto
			massaHDC = 12*self.nCarbon + HinMolec + 2*DinMolec

			# Fazendo todos os M+. e acima iguais ao valor D0
			for i in range(1, self.nMax-massaHDC+1):
				self.massSpectra[massaHDC-self.nMin+i][DinMolec] = self.massSpectra[self.MMH-self.nMin+i][0]

			# Itera para todos os possíveis números de átomos de H perdidos
			for HsPerdidos in range(HinMolec+1):
				# e também para todos os possíveis valores de átomos de D perdidos
				for DsPerdidos in range(DinMolec+1):
					# Determina a massa total perdida (H's + D's)
					massaPerdida = HsPerdidos + 2*DsPerdidos
					# Caso a massa perdida caia fora da região considerada do espectro para a iteração
					if massaPerdida > (massaHDC-self.nMin):
						break
					# Determinação do termo estatístico de perda para H, D e geral da molécula
					C1 = combin.Combinations(HinMolec, HsPerdidos).calcComb
					C2 = combin.Combinations(DinMolec, DsPerdidos).calcComb
					C3 = combin.Combinations(self.nHydrogen, HsPerdidos+DsPerdidos).calcComb
					# Correção estatística * correção fator H/D * valor no espectro de massas do peridrogenado
					# O valor no espectro de massas do peridrogenado obtido como se todos os átomos perdidos na iterção
					#(H+D) fossem átomos de H
					A = C1*C2/C3 * self.fatoreshd[DsPerdidos] * self.massSpectra[self.MMH-self.nMin-HsPerdidos-\
					DsPerdidos][0]
					# Aplica a correção a massa adequada
					self.massSpectra[massaHDC-self.nMin-massaPerdida][DinMolec] = self.massSpectra[massaHDC-self.nMin-
					massaPerdida][DinMolec] + A
		# Retorna a lista contendo o conjunto de espectros de massas
		return self.massSpectra
