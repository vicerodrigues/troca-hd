from tkinter import filedialog
import os
import arrays,spectracorr,resultsaver

class IniciaArquivo:

    def __init__(self, tipo, **kwargs):

        self.tipo = tipo
        if len(kwargs) > 0:
            self.controller = kwargs['controller']

    def AbreArquivo(self):

        #  Opções da caixa de diálogo
        self.file_opt = options = {}
        options['defaultextension'] = '.xlsx'
        options['filetypes'] = [('Excel 2007-2013', '.xlsx'), ('all files', '.*')]
        options['initialdir'] = os.path.expanduser(self.controller.openFileDir)
        options['title'] = 'Abrir espectro composto ' + self.tipo
        if self.tipo == 'peridrogenado':
            options['initialfile'] = 'PH.xlsx'
        elif self.tipo == 'perdeuterado':
            options['initialfile'] = 'PD.xlsx'
        elif self.tipo == 'mistura':
            options['initialfile'] = 'PM.xlsx'

        # Abre arquivo e passa para self.filename
        self.filename = filedialog.askopenfilename(**self.file_opt)

        self.controller.openFileDir = os.path.dirname(self.filename)
        
        if os.path.isfile(str(self.filename)):
            self.myArray =  arrays.IO_Array(self.filename).create_array(self.controller)[1:]
            self.corrArray = spectracorr.SpectraCorr(self.controller, self.myArray).correctSpec()
            return self.corrArray

    def salvarArquivo(self, fileSaveList, *args):

        self.outputList = fileSaveList

        self.args = args

        #  Opções da caixa de diálogo
        self.file_opt = options = {}
        options['defaultextension'] = '.xlsx'
        options['filetypes'] = [('Excel 2007-2013', '.xlsx')]
        options['initialdir'] = os.path.expanduser(self.controller.saveFileDir)
        if self.tipo == 'MSsave':
            options['title'] = 'Salvar espectros'
            options['initialfile'] = 'MSspectra.xlsx'
        elif self.tipo == 'Resultsave':
            options['title'] = 'Salvar resultados'
            options['initialfile'] = 'Resultados.xlsx'

        # Abre arquivo e passa para self.filename
        self.filename = filedialog.asksaveasfilename(**self.file_opt)

        self.controller.saveFileDir = os.path.dirname(self.filename)

        if self.filename != '':
            if self.tipo == 'MSsave':
                arrays.IO_Array(self.filename).export_array(self.outputList)
            elif self.tipo == 'Resultsave':
                resultsaver.OutputResults(self.filename).export_results(self.outputList, self.args)

