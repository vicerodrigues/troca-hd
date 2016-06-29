from molecula import frmolec
from files import frfiles
from menu import frmenu


class CalculaFatoresHD:
	"""Módulo que calcula os fatores de perda H/D necessários para o cálculos dos espectros de massas dos diferentes
		compostos deuterados.
	"""

	def __init__(self, controller):

		#Inicializando variáveis locais
		self.controller = controller

		self.MMH = self.controller.frames[frmolec.FrameIniciaMolecula].myMMH.get()
		self.MMD = self.controller.frames[frmolec.FrameIniciaMolecula].myMMD.get()
		self.peridrogenado = self.controller.frames[frfiles.FrameAbreArquivos].peridrogenado
		# Determina a disponibilidade do espectro de massas do composto perdeuterado
		if self.controller.frames[frmenu.MyMenu].perdeutCheck.get() == 1:
			self.perdeuterado = self.controller.frames[frfiles.FrameAbreArquivos].perdeuterado
		self.nMin = self.controller.frames[frmolec.FrameIniciaMolecula].mySpecMin.get()

	def fatoresHD(self):
		"""Função que de fato calcula a matriz de fatores de perda H/D.
		"""

		# Determina o número de fatores que necessitam ser calculados
		self.nFactors = int((self.MMD-self.nMin)/2)
		# Inicializa uma lista vazia
		self.fatores = []
		# O primeiro fator é para perda de 0 átomos e por isso é 1.0
		self.fatores.append(1.0)
		# Determina se o espectro perdeuterado será utilizado
		if self.controller.frames[frmenu.MyMenu].perdeutCheck.get() == 1:
			for i in range(self.nFactors):
				# O fator é a razão entre a intensidade dos picos nos espectros perdeuterado/peridrogenado
				self.fatores.append(self.perdeuterado[self.MMD-2*(i+1)-self.nMin]/self.peridrogenado[self.MMH-(i+1)-self.nMin])
		else:
			for i in range(self.nFactors):
				# Caso o espectro perdeuterado não esteja disponível, é utilizado um valor médio.
				self.fatores.append(0.65)
		return self.fatores