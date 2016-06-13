class IniciaMolecula:
    """Classe para calcular os valores das massas moleculares do compostos peridrogenado
        e perdeuterado, além do número de massas a serem considerados nos espectros.
        Também possui funções que tratam as entradas do software em frmolec.
    """

    def __init__(self, nCarbon, nHydrogen, nMin, nMax, frame1, mySpecWarn, mySupraWarn, myMetilaWarn, myFaixaWarn):

        self.nMin = nMin
        self.nMax = nMax
        self.nCarbon = nCarbon
        self.nHydrogen = nHydrogen
        self.frame1 = frame1
        self.mySpecWarn = mySpecWarn
        self.mySupraWarn = mySupraWarn
        self.myMetilaWarn = myMetilaWarn
        self.myFaixaWarn = myFaixaWarn

        # retornando os valores solicitados a classe.
        self.MMH = 12 * self.nCarbon + self.nHydrogen
        self.MMD = 12 * self.nCarbon + 2 * self.nHydrogen
        self.nPoints = self.nMax - self.nMin + 1

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
                self.frame1.WriteLog('error', 'Cuidado! A massa mínima do espectro não pode ser maior que a máxima.')
                self.frame1.WriteLog('warn', 'Ajustando automaticamente o valor')
        return self.nMin

    def issueWarnings(self):

        if self.nPoints <= self.nHydrogen+1 and not self.mySupraWarn:
            self.mySupraWarn = True
            self.frame1.WriteLog('error', "Sistema supra-determinado: O número mínimo de pontos a serem "
                                         "considerados deve ser maior que o número de H's +1")
        if self.nMin <= max(self.MMD-18, self.MMH-15) and not self.myMetilaWarn:
            self.myMetilaWarn = True
            self.frame1.WriteLog('warn', 'No caso de moléculas terminadas em grupos CH3 (Ex.: propano ou metil '
                                         'benzeno), pode estar havendo sobreposição do espectro considerado com o '
                                         'espectro de M-15.')
            self.frame1.WriteLog('warn', 'Sugere-se aumentar o valor do limite mínimo do espectro de massas.')
        if not ((self.nMin <= self.MMH-3) and (self.nMax >= self.MMD+2)) and not self.myFaixaWarn:
            self.myFaixaWarn = True
            self.frame1.WriteLog('warn', 'De modo a melhorar a qualidade da simulação sugere-se utiliza faixa '
                                         'do espectro de massas contendo (MMH-3) e (MMD+2).')