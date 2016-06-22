import frmolec,frfiles,frmenu

class CalculaFatoresHD:

	def __init__(self, controller):

		self.controller = controller

		self.MMH = self.controller.frames[frmolec.FrameIniciaMolecula].myMMH.get()
		self.MMD = self.controller.frames[frmolec.FrameIniciaMolecula].myMMD.get()
		self.peridrogenado = self.controller.frames[frfiles.FrameAbreArquivos].peridrogenado
		if self.controller.frames[frmenu.MyMenu].perdeutCheck.get() == 1:
			self.perdeuterado = self.controller.frames[frfiles.FrameAbreArquivos].perdeuterado
		self.nMin = self.controller.frames[frmolec.FrameIniciaMolecula].mySpecMin.get()

	def fatoresHD(self):

		self.nFactors = int((self.MMD-self.nMin)/2)
		self.fatores = []
		self.fatores.append(1.0)
		if self.controller.frames[frmenu.MyMenu].perdeutCheck.get() == 1:
			for i in range(self.nFactors):
				self.fatores.append(self.perdeuterado[self.MMD-2*(i+1)-self.nMin]/self.peridrogenado[self.MMH-(i+1)-self.nMin])
		else:
			for i in range(self.nFactors):
				self.fatores.append(0.65)
		return self.fatores