from tkinter import filedialog
import os
import numpy as np
import openpyxl


class IniciaArquivo:

    def __init__(self):

        #  Opções da caixa de diálogo
        self.file_opt = options = {}
        options['defaultextension'] = '.xls'
        options['filetypes'] = [('Excel 2003', '.xls'), ('Excel 2007-2013', '.xlsx'), ('all files', '.*')]
        options['initialdir'] = os.path.expanduser('~/git/troca-hd/examples')
        options['title'] = 'Abrir espectro composto peridrogenado'
        options['initialfile'] = 'PH.xls'

        # Abre arquivo e passa para self.filename
        self.filename = filedialog.askopenfilename(**self.file_opt)
