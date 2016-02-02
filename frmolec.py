from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
import molec
import c13matrix
import logging


class FrameIniciaMolecula(ttk.Frame):
    """Esta classe cria o frame onde é iniciada a molécula CxHy e os limites do espectro
        de massas. São carregados também os widgets que retornam as massas e o número
        de massas consideradas.
    """

    def __init__(self, parent, controller, frame1, frame2, check):
        ttk.Frame.__init__(self, parent)

        # Esta variável passada pela classe principal é a instância do logframe e permite
        # escrever no log.
        self.frame1 = frame1
        self.frame1.WriteLog('info', 'Iniciando Frames de descrição da molécula e espectro.')

        # Esta variável passada pela classe principal é a instância de frame de abrir arquivos e permite
        # que frmolec interaja com os botões habilitando-os
        self.frame2 = frame2

        # Boolean contendo o uso do espectro perdeuterado:
        self.check = check

        # Inicia o frame da classe
        self.iniciaMolec = ttk.Frame(self, padding=(5, 5, 5, 5), relief=RIDGE, borderwidth=2)
        self.iniciaMolec.grid(row=0, column=0, sticky=(N, S, E, W), padx=2, pady=2)

        # Três frames internos para ajudar no alinhamento independente
        self.molecFrame = ttk.Frame(self.iniciaMolec)
        self.molecFrame.grid(row=0, column=0, sticky=W)
        self.specFrame = ttk.Frame(self.iniciaMolec)
        self.specFrame.grid(row=1, column=0, sticky=W)
        self.massasFrame = ttk.Frame(self.iniciaMolec)
        self.massasFrame.grid(row=2, column=0, sticky=W)

        # Inicia variáveis das spinboxes contendo átomos de C e de H na molécula C6H6
        self.myCarbonNumber = IntVar()
        self.myCarbonNumber.set(6)
        self.myHydNumber = IntVar()
        self.myHydNumber.set(6)

        # Popula o primeiro frame com os dados da molécula
        self.lbl1 = ttk.Label(self.molecFrame, text='Molécula: C', padding=(0, 0, 0, 15), font='TkCaptionFont')
        self.lbl1.grid(row=0, column=0, pady=5)
        self.carbonNumber = Spinbox(self.molecFrame, from_=1, to=9, textvariable=self.myCarbonNumber, increment=1,
                                    width=1)
        self.carbonNumber.grid(row=0, column=1, pady=5)
        self.lbl2 = ttk.Label(self.molecFrame, text='H', padding=(0, 0, 0, 15), font='TkCaptionFont')
        self.lbl2.grid(row=0, column=2, pady=5)
        self.hydNumber = Spinbox(self.molecFrame, from_=1, to=20, textvariable=self.myHydNumber, increment=1,
                                 width=2)
        self.hydNumber.grid(row=0, column=3, pady=5)

        # Inicia as variáveis dos limites do espectro
        self.mySpecMin = IntVar()
        self.mySpecMin.set(73)
        self.mySpecMax = IntVar()
        self.mySpecMax.set(86)

        # Popula o segundo frame com os limites do espectro
        self.lbl3 = ttk.Label(self.specFrame, text='Limites do espectro:', font='TkCaptionFont')
        self.lbl3.grid(row=0, column=0, padx=(0, 5), pady=(5, 2))
        self.specMin = Spinbox(self.specFrame, from_=10, to=155, textvariable=self.mySpecMin, increment=1, width=3)
        self.specMin.grid(row=0, column=1, pady=(5, 2))
        self.specMax = Spinbox(self.specFrame, from_=10, to=155, textvariable=self.mySpecMax, increment=1, width=3)
        self.specMax.grid(row=1, column=1, pady=(2, 5))
        self.lbl4 = ttk.Label(self.specFrame, text='min.', font='TkSmallCaptionFont')
        self.lbl4.grid(row=0, column=3, pady=(5, 2))
        self.lbl5 = ttk.Label(self.specFrame, text='max.', font='TkSmallCaptionFont')
        self.lbl5.grid(row=1, column=3, pady=(2, 5))

        # Inicia as variáveis das massas moleculares e número de pontos
        self.frame1.WriteLog('info', 'Calculando massas moleculares e número de pontos.')

        self.myMMH = IntVar()
        self.myMMD = IntVar()
        self.nPoints = IntVar()

        # Variáveis booleanas para lançamentos de erros repetitivos
        self.mySpecWarn = False
        self.mySupraWarn = False
        self.myMetilaWarn = False
        self.myFaixaWarn = False

        # Atualiza os valores das massas moleculare e número de pontos
        self.AtualizaValores()

        # Widgets das massas e número de pontos:
        self.lbl6 = ttk.Label(self.massasFrame, text='Massas Moleculares:', font='TkCaptionFont')
        self.lbl6.grid(row=2, column=0, columnspan=2, padx=(0, 5), pady=(5, 2))
        self.lbl7 = ttk.Label(self.massasFrame, text='-Peridrogenado:')
        self.lbl7.grid(row=3, column=1, sticky=W, pady=(2, 2))
        self.lbl8 = ttk.Label(self.massasFrame, text='-Perdeuterado:')
        self.lbl8.grid(row=4, column=1, sticky=W, pady=(2, 5))
        self.lbl9 = ttk.Label(self.massasFrame, text='Pontos considerados:', font='TkCaptionFont')
        self.lbl9.grid(row=5, column=0, columnspan=2, padx=(0, 5), pady=5)
        self.myMMHLbl = ttk.Label(self.massasFrame, textvariable=self.myMMH)
        self.myMMHLbl.grid(row=3, column=2, padx=10, pady=(2, 2))
        self.myMMDLbl = ttk.Label(self.massasFrame, textvariable=self.myMMD)
        self.myMMDLbl.grid(row=4, column=2, padx=10, pady=(2, 5))
        self.nPointsLbl = ttk.Label(self.massasFrame, textvariable=self.nPoints)
        self.nPointsLbl.grid(row=5, column=2, padx=10, pady=5)

        # Botão Aceitar molécula que leva ao cálculo da matriz de contribuição de 13C e libera o acesso a seleção
        # de arquivos
        self.btnAceitar = ttk.Button(self.iniciaMolec, text='Aceitar', command=self.AceitaMolecula)
        self.btnAceitar.bind('<Return>', self.AceitaMolecula)
        self.btnAceitar.grid(row=3, column=0)
        self.btnAceitar.focus_force()

        # Funções de trace acompanhando os números de átomos de carbono e hidrogênio
        # e os valores de máximo e mínimo do espectro
        self.myCarbonNumber.trace('w', self.AtualizaValores)
        self.myHydNumber.trace('w', self.AtualizaValores)
        self.mySpecMin.trace('w', self.AtualizaValores)
        self.mySpecMax.trace('w', self.AtualizaValores)

    def AtualizaValores(self, *args):
        """Função responsável por importar o módulo molec atualizar os valores das massas
            moleculares e do número de massas a serem consideradas.
            Chama também a função CorrigeLimites do módulo molec que não permite que
            mySpecMin seja maior que mySpecMax.
        """

        # INFO: Adicionar aqui algum mecanismo para que escreva o log só na primeira mudança!

        myMolec = molec.IniciaMolecula(self.myCarbonNumber.get(), self.myHydNumber.get(), self.mySpecMin.get(),
                                       self.mySpecMax.get(), self.frame1, self.mySpecWarn, self.mySupraWarn,
                                       self.myMetilaWarn, self.myFaixaWarn)
        self.myMMH.set(myMolec.MMH)
        self.myMMD.set(myMolec.MMD)
        self.nPoints.set(myMolec.nPoints)
        # redefine o valor de SpecMin para que não sobrepuje SpecMax
        self.mySpecMin.set(myMolec.CorrigeLimites)
        myMolec.issueWarnings()
        self.mySpecWarn = myMolec.mySpecWarn
        self.mySupraWarn = myMolec.mySupraWarn
        self.myMetilaWarn = myMolec.myMetilaWarn
        self.myFaixaWarn = myMolec.myFaixaWarn

        # Exemplo de log:
        # self.frame1.WriteLog('info', 'I Rock too')

    def AceitaMolecula(self, *args):
        """Função ligada ao botão Aceitar da descrição da molécula. Deve dar início ao cálculo da matriz de
            contribuições de 13C e liberar o acesso ao Frame de abertura de arquivos de massas. Se for pressionado
            dando origem a um sistema supra-deteerminado retorna uma caixa de erro.
        """

        while True:

            # Lança erro para um sistema supra-determinado e não executa o resto da função.
            if self.nPoints.get() <= self.myHydNumber.get()+1:
                messagebox.showinfo(title='Erro', message='Sistema supra-determinado', detail="O número mínimo de \
pontos a serem considerados deve ser maior que o número de H's +1", icon='error')
                self.frame1.text_handler.setFormatter(logging.Formatter('%(message)s'))
                self.frame1.WriteLog('info', ' '*11+'Inicializando molécula:'+' '*11+'\n'*2)
                self.frame1.text_handler.setFormatter(logging.Formatter(self.frame1.format_))
                self.frame1.WriteLog('critical', "Sistema supra-determinado: O número mínimo de pontos a serem "
                                                 "considerados deve ser maior que o número de H's +1")
                self.frame1.WriteLog('critical', 'Não será dado prosseguimento a execução do programa!')
                self.frame1.WriteLog('info', 'Corrija o número de pontos e clique em aceitar novamente.')
                break

            # Descreve a molécula e o espectro no log.
            self.frame1.text_handler.setFormatter(logging.Formatter('%(message)s'))
            self.frame1.WriteLog('info', ' '*11+'Inicializando molécula:'+' '*11+'\n'*2)
            self.frame1.text_handler.setFormatter(logging.Formatter(self.frame1.format_))
            self.frame1.WriteLog('info', 'Molécula: C%iH%i\n     Espectro: -Min:%i\n               -Max:%i' %(self.\
myCarbonNumber.get(), self.myHydNumber.get(), self.mySpecMin.get(), self.mySpecMax.get()))

            # Anuncia o cálculo da matriz de 13C
            self.frame1.WriteLog('info', 'Calculando a matriz de contribuições de 13C na molécula.')
            # Resgata o valor da Matriz de 13C do módulo c13matrix
            self.myC13Matrix = c13matrix.C13Matrix(self.myCarbonNumber.get()).CalcC13Matrix

            self.frame1.WriteLog('info', 'Imprimindo a matrix de contribuições de 13C:')
            self.frame1.text_handler.setFormatter(logging.Formatter('%(message)s'))

            for i in range(self.myCarbonNumber.get()+1):
                self.frame1.WriteLog('info', ' '*7 + '13C [%i]:' %i + '%.10f' %self.myC13Matrix[i] + '\n')
            self.frame1.WriteLog('info', '\n')
            self.frame1.text_handler.setFormatter(logging.Formatter(self.frame1.format_))

            self.frame1.WriteLog('info', 'Habilitando os botões para abrir os arquivos de espectros de massas')

            # habilitando os botões
            self.frame2.btnAbrePeridrogenado.configure(state='enabled')
            self.frame2.btnAbreMistura.configure(state='enabled')

            # colocar aqui um if para somente liberar este botão caso esteja marcada a opção de utilizar o espectro
            # perdeuterado.

            if self.check:
                self.frame2.btnAbrePerdeuterado.configure(state='enabled')

            self.frame2.btnAbrePeridrogenado.focus_force()

            break
