import frmolec
import numpy as np

class SpectraCorr:

	def __init__(self, controller, array):

		self.controller = controller
		self.array = array

		self.MMD = self.controller.frames[frmolec.FrameIniciaMolecula].myMMD.get()
		self.nMin = self.controller.frames[frmolec.FrameIniciaMolecula].mySpecMin.get()
		self.C13Matrix = self.controller.frames[frmolec.FrameIniciaMolecula].myC13Matrix

	def correctSpec(self):

		for i in range(self.MMD-self.nMin+1):
			self.array[i] = np.divide(self.array[i],np.array(self.C13Matrix[0]))
			for j in range(1, len(self.C13Matrix)):
				if (i+j) >= len(self.array):
					break
				self.array[i+j] = self.array[i+j] - self.C13Matrix[j]*self.array[i]

		return self.array
