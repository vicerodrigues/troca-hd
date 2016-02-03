from tkinter import *
from tkinter import ttk
# from tkinter import filedialog


class FrameAbreArquivos(ttk.Frame):
    """Esta classe cria o frame onde é são abertos os arquivos contendo os espectros de massas dos compostos
        peridrogenado, perdeuterado e da mistura. É também feita a correção da contribuição de 13C no espectro
        através do módulo ......
    """

    def __init__(self, parent, controller, frame1):
        ttk.Frame.__init__(self, parent)

        # Esta variável passada pela classe principal é a instância do logframe e permite
        # escrever no log.
        self.frame1 = frame1
        self.frame1.WriteLog('info', 'Iniciando Frames de abertura dos arquivos contendo os espectros de massas.')

        # Iniciando o frame da classe
        self.abreArquivos = ttk.Frame(self, padding=(5, 5, 5, 5), relief=RIDGE, borderwidth=2)
        self.abreArquivos.grid(row=0, column=0, sticky=(N, S, E, W), padx=2, pady=2)

        # Label para o titulo do frame
        self.labelAbreArquivos = ttk.Label(self.abreArquivos, text='Espectros de massas:', font='TkCaptionFont')
        self.labelAbreArquivos.grid(row=0, column=0, columnspan=3, sticky=W, pady=(5, 5))

        # Três frames internos para ajudar na separação e alinhamento
        # Para mudar o estilo do texto em Labelframe criar uma Label como:
        # self.l1 = ttk.Label(text='Peridrogenado:', font='TkCaptionFont')
        # e passá-la ao atributo textwidget=self.l1
        self.abrePeridrogenado = ttk.Labelframe(self.abreArquivos, text='Peridrogenado:', padding=(10, 10, 10, 10))
        self.abrePeridrogenado.grid(row=1, column=0, padx=5)
        self.abrePerdeuterado = ttk.Labelframe(self.abreArquivos, text='Perdeuterado:', padding=(10, 10, 10, 10))
        self.abrePerdeuterado.grid(row=1, column=1, padx=5)
        self.abreMistura = ttk.Labelframe(self.abreArquivos, text='Mistura:', padding=(10, 10, 10, 10))
        self.abreMistura.grid(row=1, column=2, padx=5)

        # Popula os frames de abertura de arquivos
        self.btnAbrePeridrogenado = ttk.Button(self.abrePeridrogenado, text='Abrir')
        self.btnAbrePeridrogenado.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        self.btnAbrePeridrogenado.configure(state='disabled')
        self.espectroPeridrogenado = Text(self.abrePeridrogenado, width=15, height=10, wrap='none')
        self.espectroPeridrogenado.grid(row=1, column=0)
        self.espectroPeridrogenado.configure(state='disabled')

        # Criando a ScrollBar e associando a TextBox
        self.espectroPeridrogenadoScrollV = ttk.Scrollbar(self.abrePeridrogenado, orient=VERTICAL,
                                                         command=self.espectroPeridrogenado.yview)
        self.espectroPeridrogenadoScrollV.grid(row=1, column=1, sticky=(N, S))
        self.espectroPeridrogenado['yscrollcommand'] = self.espectroPeridrogenadoScrollV.set
        self.espectroPeridrogenadoScrollH = ttk.Scrollbar(self.abrePeridrogenado, orient=HORIZONTAL,
                                                         command=self.espectroPeridrogenado.xview)
        self.espectroPeridrogenadoScrollH.grid(row=2, column=0, sticky=(E, W))
        self.espectroPeridrogenado['xscrollcommand'] = self.espectroPeridrogenadoScrollH.set

        # Popula os frames de abertura de arquivos
        self.btnAbrePerdeuterado = ttk.Button(self.abrePerdeuterado, text='Abrir')
        self.btnAbrePerdeuterado.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        self.btnAbrePerdeuterado.configure(state='disabled')
        self.espectroPerdeuterado = Text(self.abrePerdeuterado, width=15, height=10, wrap='none')
        self.espectroPerdeuterado.grid(row=1, column=0)
        self.espectroPerdeuterado.configure(state='disabled')

        # Criando a ScrollBar e associando a TextBox
        self.espectroPerdeuteradoScrollV = ttk.Scrollbar(self.abrePerdeuterado, orient=VERTICAL,
                                                         command=self.espectroPerdeuterado.yview)
        self.espectroPerdeuteradoScrollV.grid(row=1, column=1, sticky=(N, S))
        self.espectroPerdeuterado['yscrollcommand'] = self.espectroPerdeuteradoScrollV.set
        self.espectroPerdeuteradoScrollH = ttk.Scrollbar(self.abrePerdeuterado, orient=HORIZONTAL,
                                                         command=self.espectroPerdeuterado.xview)
        self.espectroPerdeuteradoScrollH.grid(row=2, column=0, sticky=(E, W))
        self.espectroPerdeuterado['xscrollcommand'] = self.espectroPerdeuteradoScrollH.set

        # Popula os frames de abertura de arquivos
        self.btnAbreMistura = ttk.Button(self.abreMistura, text='Abrir')
        self.btnAbreMistura.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        self.btnAbreMistura.configure(state='disabled')
        self.espectroMistura = Text(self.abreMistura, width=15, height=10, wrap='none')
        self.espectroMistura.grid(row=1, column=0)
        self.espectroMistura.configure(state='disabled')

        # Criando a ScrollBar e associando a TextBox
        self.espectroMisturaScrollV = ttk.Scrollbar(self.abreMistura, orient=VERTICAL,
                                                         command=self.espectroMistura.yview)
        self.espectroMisturaScrollV.grid(row=1, column=1, sticky=(N, S))
        self.espectroMistura['yscrollcommand'] = self.espectroMisturaScrollV.set
        self.espectroMisturaScrollH = ttk.Scrollbar(self.abreMistura, orient=HORIZONTAL,
                                                         command=self.espectroMistura.xview)
        self.espectroMisturaScrollH.grid(row=2, column=0, sticky=(E, W))
        self.espectroMistura['xscrollcommand'] = self.espectroMisturaScrollH.set

