import frlog

class IniciaMolecula:
    """Classe para calcular os valores das massas moleculares do compostos peridrogenado
        e perdeuterado, além do número de massas a serem considerados nos espectros.
        Também possui funções que tratam as entradas do software em frmolec.
    """

    def __init__(self, controller, nCarbon, nHydrogen, nMin, nMax, mySpecWarn, mySupraWarn, myMetilaWarn, \
                 myFaixaWarn, myNMinWarn):

        self.controller = controller
        self.nMin = nMin
        self.nMax = nMax
        self.nCarbon = nCarbon
        self.nHydrogen = nHydrogen
        self.mySpecWarn = mySpecWarn
        self.mySupraWarn = mySupraWarn
        self.myMetilaWarn = myMetilaWarn
        self.myFaixaWarn = myFaixaWarn
        self.myNMinWarn = myNMinWarn

        # retornando os valores solicitados a classe.
        self.MMH = 12 * self.nCarbon + self.nHydrogen
        self.MMD = 12 * self.nCarbon + 2 * self.nHydrogen
        self.nPoints = self.nMax - self.nMin + 1

    # Permite chamar a função como sendo uma propriedade que retorna um inteiro
    @property
    def CorrigeLimites(self):
        """Função que corrige os limites do espectros de massas de modo que SpecMin não
            seja maior que SpecMax.
            return type: Integer
        """

        if self.nMin >= self.nMax:
            self.nMin = self.nMax - 1
            if not self.mySpecWarn:
                self.mySpecWarn = True
                self.controller.frames[frlog.FrameLog].WriteLog('error', 'Cuidado! A massa mínima do espectro não pode ser maior que a máxima.')
                self.controller.frames[frlog.FrameLog].WriteLog('warn', 'Ajustando automaticamente o valor')
        return self.nMin

    def issueWarnings(self):
        """Função que faz uma série de observações e lança warnings sobre as melhores práticas na escolha da faixa de 
            massas a ser utilizada nos espectros.
        """

        # Sistema supra-determinado
        if self.nPoints <= self.nHydrogen+1 and not self.mySupraWarn:
            self.mySupraWarn = True
            self.controller.frames[frlog.FrameLog].WriteLog('error', "Sistema supra-determinado: O número mínimo de pontos a serem "
                                         "considerados deve ser maior que o número de H's +1")
        # Utilização de M-15 em moléculas com grupos metila
        if self.nMin <= max(self.MMD-18, self.MMH-15) and not self.myMetilaWarn:
            self.myMetilaWarn = True
            self.controller.frames[frlog.FrameLog].WriteLog('warn', 'No caso de moléculas terminadas em grupos CH3 (Ex.: propano ou metil '
                                         'benzeno), pode estar havendo sobreposição do espectro considerado com o '
                                         'espectro de M-15.')
            self.controller.frames[frlog.FrameLog].WriteLog('warn', 'Sugere-se aumentar o valor do limite mínimo do espectro de massas.')
        # Faixa recomendada do espectro
        if not ((self.nMin <= self.MMH-3) and (self.nMax >= self.MMD+2)) and not self.myFaixaWarn:
            self.myFaixaWarn = True
            self.controller.frames[frlog.FrameLog].WriteLog('warn', 'De modo a melhorar a qualidade da simulação sugere-se utiliza faixa '
                                         'do espectro de massas contendo pelo menos entre (MMH-3) e (MMD+2).')
        # Faixa utilizada abaixo de todas as perdas de Hidrogênio
        if self.nMin < (self.MMH-self.nHydrogen) and not self.myNMinWarn:
            self.myNMinWarn = True
            self.controller.frames[frlog.FrameLog].WriteLog('warn', 'A faixa escolhida do espectro transcende a faixa de perda dos hidrogênios'
                                         ' da molécula. Recomenda-se usar (MMH-nHydrogen) para o mínimo.')