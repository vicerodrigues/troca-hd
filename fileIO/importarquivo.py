from tkinter import filedialog
import os
from log import frlog
from fileIO import arrays,spectracorr,resultsaver


class IniciaArquivo:
    """Esta classe chama as janelas de escolha de arquivos, chamando as funções apropriadas para leitura e salvamento
        dos dados. No caso de abertura dos arquivos ainda instancia a classe que corrige para as contribuições de 13C, 
        retornando a frfiles o espectro já corrigido.  
    """

    def __init__(self, tipo, **kwargs):

        # Inicialização da classe e atribuição de variáveis.
        self.tipo = tipo
        # Inicialmente controller seria uma variável opcional para algumas instâncias (o que mudou depois) e por isso 
        #é inicializada assim.
        if len(kwargs) > 0:
            self.controller = kwargs['controller']

    def AbreArquivo(self):
        """Função que de chama a caixa de diálogo de abertura de arquivo e o passa para o módulo arrays que de fato 
            recupera os dados. Em seguida chama o módulo de correção de 13C e devolve os dados para frfiles. 
        """

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
        # Identificando o arquivo aberto no log
        if self.filename != '':
            self.controller.frames[frlog.FrameLog].WriteLog('info', 'Arquivo: %s' %self.filename)
        else:
            self.controller.frames[frlog.FrameLog].WriteLog('warn', 'Abertura de arquivo cancelada')            

        # Faz o update da variável que contém o último diretório aberto
        self.controller.openFileDir = os.path.dirname(self.filename)
        
        # Função if que identifica se algum arquivo foi escolhido
        if os.path.isfile(str(self.filename)):
            # caso sim abre o arquivo e corrige o espectro
            self.myArray =  arrays.IO_Array(self.filename).create_array(self.controller)[1:]
            self.controller.frames[frlog.FrameLog].WriteLog('info', 'Calculando as correções das matriz de 13C.')
            self.corrArray = spectracorr.SpectraCorr(self.controller, self.myArray).correctSpec()
            return self.corrArray

    def salvarArquivo(self, fileSaveList, *args):
        """Função que de chama a caixa de diálogo de salvamento de arquivo e o passa para o módulo adequado que de
            fato salvará os dados.
        """

        # Inicializa variáveis locais
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
            
        # Faz o update da variável que contém o último diretório aberto
        self.controller.saveFileDir = os.path.dirname(self.filename)

        # Função if que identifica se algum arquivo foi escolhido
        if self.filename != '':
            # e chama os módulos adequados para o salvamento
            if self.tipo == 'MSsave':
                arrays.IO_Array(self.filename).export_array(self.outputList)
            elif self.tipo == 'Resultsave':
                # args é uma passagem de variáveis descritoras das simulação somente utilizada ao salvar os resultados. 
                resultsaver.OutputResults(self.filename).export_results(self.outputList, self.args)
            # Identificando o arquivo no Log
            self.controller.frames[frlog.FrameLog].WriteLog('info', 'Arquivo: %s' %self.filename)
            self.controller.frames[frlog.FrameLog].WriteLog('info', 'Arquivo salvo com sucesso.')
        else:
            self.controller.frames[frlog.FrameLog].WriteLog('warn', 'Salvamento de arquivo cancelado')