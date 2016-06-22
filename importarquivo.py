from tkinter import filedialog
import os
import arrays,spectracorr

class IniciaArquivo:

    def __init__(self, tipo, controller):

        self.tipo = tipo
        self.controller = controller

    def AbreArquivo(self):

        #  Opções da caixa de diálogo
        self.file_opt = options = {}
        options['defaultextension'] = '.xlsx'
        options['filetypes'] = [('Excel 2007-2013', '.xlsx'), ('all files', '.*')]
        options['initialdir'] = os.path.expanduser('~/git/troca-hd/examples')
        options['title'] = 'Abrir espectro composto ' + self.tipo
        if self.tipo == 'peridrogenado':
            options['initialfile'] = 'PH.xlsx'
        elif self.tipo == 'perdeuterado':
            options['initialfile'] = 'PD.xlsx'
        elif self.tipo == 'mistura':
            options['initialfile'] = 'PM.xlsx'

        # Abre arquivo e passa para self.filename
        self.filename = filedialog.askopenfilename(**self.file_opt)

        self.myArray =  arrays.IO_Array(self.filename).create_array()[1:]

        self.corrArray = spectracorr.SpectraCorr(self.controller, self.myArray).correctSpec()

        return self.corrArray

    def salvarArquivo(self, fileSaveList):

        self.massSpectra = fileSaveList

        #  Opções da caixa de diálogo
        self.file_opt = options = {}
        options['defaultextension'] = '.xlsx'
        options['filetypes'] = [('Excel 2007-2013', '.xlsx')]
        options['initialdir'] = os.path.expanduser('~/git/troca-hd/examples')
        options['title'] = 'Salvar espectros'
        options['initialfile'] = 'MSspectra.xlsx'

        # Abre arquivo e passa para self.filename
        self.filename = filedialog.asksaveasfilename(**self.file_opt)

        arrays.IO_Array(self.filename).export_array(self.massSpectra)
