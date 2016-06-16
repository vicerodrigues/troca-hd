from tkinter import filedialog
import os
import arrays

class IniciaArquivo:

    def __init__(self, tipo):

        self.tipo = tipo

    def AbreArquivo(self):

        #  Opções da caixa de diálogo
        self.file_opt = options = {}
        options['defaultextension'] = '.xlsx'
        options['filetypes'] = [('Excel 2007-2013', '.xlsx'), ('all files', '.*')]
        options['initialdir'] = os.path.expanduser('~/Downloads/troca-hd/examples')
        options['title'] = 'Abrir espectro composto ' + self.tipo
        options['initialfile'] = 'PH.xlsx'

        # Abre arquivo e passa para self.filename
        self.filename = filedialog.askopenfilename(**self.file_opt)

        self.myArray =  arrays.IO_Array(self.filename).create_array()

        return self.myArray