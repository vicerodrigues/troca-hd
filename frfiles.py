from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import frlog,frmenu,frmolec
import importarquivo,fatoreshd,mscalc,arrays,simulaespectro

class FrameAbreArquivos(ttk.Frame):
    """Esta classe cria o frame onde é são abertos os arquivos contendo os espectros de massas dos compostos
        peridrogenado, perdeuterado e da mistura. É também feita a correção da contribuição de 13C no espectro
        através do módulo ......
    """

    def __init__(self, parent, controller):
        # Inicia ttk.Frame de onde a presente classe herda.
        ttk.Frame.__init__(self, parent)
        # Passando a variável controller para o local
        self.controller = controller

        # Informando a inicialização do frame no Log
        self.controller.frames[frlog.FrameLog].WriteLog('info', 'Iniciando Frames de abertura dos arquivos contendo os espectros de massas.')

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
        self.abrePeridrogenado.grid(row=1, column=0, padx=(8, 6))
        self.abrePerdeuterado = ttk.Labelframe(self.abreArquivos, text='Perdeuterado:', padding=(10, 10, 10, 10))
        self.abrePerdeuterado.grid(row=1, column=1, padx=6)
        self.abreMistura = ttk.Labelframe(self.abreArquivos, text='Mistura:', padding=(10, 10, 10, 10))
        self.abreMistura.grid(row=1, column=2, padx=(6, 8))

        # Popula os frames de abertura de arquivos
        self.btnAbrePeridrogenado = ttk.Button(self.abrePeridrogenado, text='Abrir', command=lambda: self.abreEspectro\
            ('peridrogenado'))
        self.btnAbrePeridrogenado.bind('<Return>', lambda x: self.abreEspectro('peridrogenado'))
        self.btnAbrePeridrogenado.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        self.btnAbrePeridrogenado.configure(state='disabled')
        self.espectroPeridrogenado = Text(self.abrePeridrogenado, width=20, height=11, wrap='none')
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
        self.btnAbrePerdeuterado = ttk.Button(self.abrePerdeuterado, text='Abrir', command=lambda: self.abreEspectro\
            ('perdeuterado'))
        self.btnAbrePerdeuterado.bind('<Return>', lambda x: self.abreEspectro('perdeuterado'))
        self.btnAbrePerdeuterado.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        self.btnAbrePerdeuterado.configure(state='disabled')
        self.espectroPerdeuterado = Text(self.abrePerdeuterado, width=20, height=11, wrap='none')
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
        self.btnAbreMistura = ttk.Button(self.abreMistura, text='Abrir', command=lambda: self.abreEspectro\
            ('mistura'))
        self.btnAbreMistura.bind('<Return>', lambda x: self.abreEspectro('mistura'))
        self.btnAbreMistura.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        self.btnAbreMistura.configure(state='disabled')
        self.espectroMistura = Text(self.abreMistura, width=20, height=11, wrap='none')
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

        # Variáveis de padding do botões
        self.myPadX = 35
        self.myPadY = 5

        # Adicionando os botões de Cálculo dos espectros, salvar espectros e simular mistura
        self.btnCalcEspectros = ttk.Button(self.abreArquivos, text='Calcular espectros', command=lambda: \
            self.trataEspectros(), state='disabled')
        self.btnCalcEspectros.bind('<Return>', lambda x: self.trataEspectros())
        self.btnCalcEspectros.grid(row=3, column=0, padx=(self.myPadX,self.myPadX), pady=(self.myPadY,self.myPadY-5)\
            , sticky='EW')

        self.btnSaveMS = ttk.Button(self.abreArquivos, text='Salvar MS', command=lambda: self.salvarMS(),\
             state='disabled')
        self.btnSaveMS.bind('<Return>', lambda x: self.salvarMS())
        self.btnSaveMS.grid(row=3, column=1, padx=(self.myPadX,self.myPadX), pady=(self.myPadY,self.myPadY-5)\
            , sticky='EW')

        self.btnSimular = ttk.Button(self.abreArquivos, text='Simular', command=lambda: self.simularEspectros(),\
             state='disabled')
        self.btnSimular.bind('<Return>', lambda x: self.simularEspectros())
        self.btnSimular.grid(row=3, column=2, padx=(self.myPadX,self.myPadX), pady=(self.myPadY,self.myPadY-5)\
            , sticky='EW')

    def AtualizaPerdeutCheck(self):
        """Função que cuida da lógica de disponibilidade da abertura do espectro de massas do composto perdeuterado,
            de acordo com a opção definida no menu.
        """

        # Somente faz algo caso a molécula tenha sido aceita e os botões de abrir os arquivos estejam disponíveis
        if self.controller.frames[frmolec.FrameIniciaMolecula].acceptedMolec == True:
            # Habilita o botão de abertura do espectro caso necessário
            if self.controller.frames[frmenu.MyMenu].perdeutCheck.get() == 1:
                self.btnAbrePerdeuterado.configure(state='enabled')
            # Desabilita o botão e apaga um espectro que porventura tenha sido aberto
            elif self.controller.frames[frmenu.MyMenu].perdeutCheck.get() ==0:
                self.btnAbrePerdeuterado.configure(state='disabled')
                self.espectroPerdeuterado.configure(state='normal')
                self.espectroPerdeuterado.delete(1.0, END)
                self.espectroPerdeuterado.configure(state='disabled')
                # Re-trata os espectros caso isso já tivesse sido feito anteriormente, agora excluindo o espectro
                #perdeuterado.
                if (self.espectroPeridrogenado.get(1.0, END) != '\n') & (self.espectroMistura.get(1.0, END) != '\n'):
                    self.trataEspectros()
            else:
                raise ValueError('Problemas com o checkbutton que controla o uso do espectro perdeuterado.')
        # Chama a função de checagem que toma conta da lógica de habilitação do botões inferiores do frame.
        self.checkTratarEspectros()
    
    def abreEspectro(self, tipo):
        """Função que cuida da abertura dos espectros de massas dos três tipos de compostos e os atribui a variáveis.
            Além disso ainda "chama" funções auxiliares que cuidam da escrita no widget de texto, habilitar botões e
            corrigir a contribuição de 13C.
        """

        # Determina qual espectro está sendo aberto
        self.tipo = tipo
        # Conjunto dos possíveis espectros
        self.compostos = ['peridrogenado','perdeuterado','mistura']
        # Escreve no log a intenção de abrir o espectro
        self.controller.frames[frlog.FrameLog].WriteLog('info', 'Abrindo arquivo referente ao espectro %s.' %self.tipo)
        # Verifica para erros internos
        if self.tipo not in self.compostos:
            self.controller.frames[frlog.FrameLog].WriteLog('critical', 'Tipo de espectro inesperado!')
        else:
            # Determina qual espectro está sendo inicializado e o associa ao widget text correto
            if self.tipo == 'peridrogenado':
                self.myWidgetSpectra = self.espectroPeridrogenado
            elif self.tipo == 'perdeuterado':
                self.myWidgetSpectra = self.espectroPerdeuterado
            else:
                self.myWidgetSpectra = self.espectroMistura
            # Instancia a classe que abre o arquivo e corrige os espectros
            self.mySpectra = importarquivo.IniciaArquivo(tipo, controller=self.controller).AbreArquivo()
            # Apaga um espectro antigo que possa estar no widget Text
            self.myWidgetSpectra.configure(state='normal')
            self.myWidgetSpectra.delete(1.0, END)
            self.myWidgetSpectra.configure(state='disabled')
            # Esta lógica verifica se o espectro tem o tamanho correto, decide para qual botão irá passar o foco e 
            #passa os espectros abertos para as variáveis corretas
            if self.mySpectra != None:
                if len(self.mySpectra) == self.controller.frames[frmolec.FrameIniciaMolecula].nPoints.get():
                    self.populaTextbox()
                    if self.tipo == 'peridrogenado':
                        if self.controller.frames[frmenu.MyMenu].perdeutCheck.get() == 1:
                            self.btnAbrePerdeuterado.focus_force()
                        else:
                            self.btnAbreMistura.focus_force()
                        self.peridrogenado = self.mySpectra
                    elif self.tipo == 'perdeuterado':
                        self.btnAbreMistura.focus_force()
                        self.perdeuterado = self.mySpectra
                    else:
                        self.mistura = self.mySpectra                    
                else:
                    self.controller.frames[frlog.FrameLog].WriteLog('error',\
                         'O tamanho do espectro não condiz com o esperado! Verifique a faixa do espectro e o arquivo.')
            # Chama a função que checa quais espectros já foram abertos para habilitar os botões de tratamento e simulação
            self.checkTratarEspectros()

    def populaTextbox(self):
        """Popula as Textboxes com os espectros abertos.
        """

        self.controller.frames[frlog.FrameLog].WriteLog('info', 'Arquivo do espectro %s carregado com sucesso' %self.tipo)
        self.myWidgetSpectra.configure(state='normal')
        self.myWidgetSpectra.delete(1.0, END)
        self.myWidgetSpectra.insert('end', '\n'.join('%.0f'%x for x in self.mySpectra))
        self.myWidgetSpectra.configure(state='disabled')

    def checkTratarEspectros(self):
        """Função que verifica quais espectros já foram abertos e, quando possível, habilita os botões de tratamento 
            e simulação dos espectros. 
        """

        if self.controller.frames[frmenu.MyMenu].perdeutCheck.get() == 1:
            if (self.espectroPeridrogenado.get(1.0, END) != '\n') & (self.espectroPerdeuterado.get(1.0, END)\
             != '\n') & (self.espectroMistura.get(1.0, END) != '\n'):
                self.btnCalcEspectros.configure(state='enabled')
                self.btnCalcEspectros.focus_force()
            else:
                self.btnCalcEspectros.configure(state='disabled')
                self.btnSaveMS.configure(state='disabled')
                self.btnSimular.configure(state='disabled')

        else:
            if (self.espectroPeridrogenado.get(1.0, END) != '\n') & (self.espectroMistura.get(1.0, END) != '\n'):
                self.btnCalcEspectros.configure(state='enabled')
                self.btnCalcEspectros.focus_force()
            else:
                self.btnCalcEspectros.configure(state='disabled')
                self.btnSaveMS.configure(state='disabled')
                self.btnSimular.configure(state='disabled')


    def trataEspectros(self):
        """Função que calcula (através de funções auxiliares) os fatores de perda H/D, e os espectros de massas dos 
            diferentes compostos deuterados.
        """

        self.fatoreshd = fatoreshd.CalculaFatoresHD(self.controller).fatoresHD()
        self.massSpectra = mscalc.DeuteratedSpectra(self.controller, self.peridrogenado, self.fatoreshd).CalcSpec()
        self.btnSaveMS.configure(state='enabled')
        self.btnSimular.configure(state='enabled')
        self.btnSimular.focus_force()

    def salvarMS(self):
        """Função que inicia o módulo que salva os espectros de massas dos compostos deuterados.
        """

        importarquivo.IniciaArquivo('MSsave', controller=self.controller).salvarArquivo(self.massSpectra)

    def simularEspectros(self):
        """Função que dá início a simulação do espectro da mistura e abre a janela de resultados.
        """

        simulaespectro.SimularEspectro(self.controller, self.mistura, self.massSpectra)





        
