import frmolec
import combin

class DeuteratedSpectra:

	def __init__(self, controller, peridrogenado, fatoreshd):
		
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
		
		self.rows, self.columns = self.nPoints, (self.nHydrogen+1)

		self.massSpectra = [[0 for column in range(self.columns)] for row in range(self.rows)]

		for i in range(self.nPoints):
			self.massSpectra[i][0] = self.peridrogenado[i]

		for DinMolec in range(1, self.nHydrogen+1):
			HinMolec = self.nHydrogen - DinMolec
			massaHDC = 12*self.nCarbon + HinMolec + 2*DinMolec

			## Fazendo todos os M+. e acima iguais ao D0
			for i in range(1, self.nMax-massaHDC+1):
				self.massSpectra[massaHDC-self.nMin+i][DinMolec] = self.massSpectra[self.MMH-self.nMin+i][0]

			for HsPerdidos in range(HinMolec+1):
				for DsPerdidos in range(DinMolec+1):
					massaPerdida = HsPerdidos + 2*DsPerdidos
					if massaPerdida > (massaHDC-self.nMin):
						break
					C1 = combin.Combinations(HinMolec, HsPerdidos).calcComb
					C2 = combin.Combinations(DinMolec, DsPerdidos).calcComb
					C3 = combin.Combinations(self.nHydrogen, HsPerdidos+DsPerdidos).calcComb
					A = C1*C2/C3 * self.fatoreshd[DsPerdidos] * self.massSpectra[self.MMH-self.nMin-HsPerdidos-\
					DsPerdidos][0]
					self.massSpectra[massaHDC-self.nMin-massaPerdida][DinMolec] = self.massSpectra[massaHDC-self.nMin-
					massaPerdida][DinMolec] + A

		return self.massSpectra
