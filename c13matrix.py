import combin


class C13Matrix:
    """Classe que cria a matriz de contribuições de 13C na molécula"""

    def __init__(self, myCarbonNumber):
        self.myCarbonNumber = myCarbonNumber

        # Abundância isotópica do 13C
        self._C13Prob = 0.011
        # Inicializando uma lista vazia e adicionando o elemento [0] que será substituído ao final.
        self.myC13Matrix = []
        self.myC13Matrix += [None]

    @property
    def CalcC13Matrix(self):
        """Calcula a contribuição de C13 na molécula"""

        # Defina soma das correções como zero
        self._sum = 0
        # Itera desde 1 até o número de 13C + 1 (não incluso o último)
        for i in range(1, self.myCarbonNumber+1):
            # Calcula cada elemento da matrix de 13C
            self.myC13Matrix += [(self._C13Prob**i)*combin.Combinations(self.myCarbonNumber, i).calcComb]
            # adiciona a soma
            self._sum += self.myC13Matrix[i]
        # calcula o aumento da probabilidade da massa zero
        self.myC13Matrix[0] = 1-self._sum
        # retorna o valor
        return self.myC13Matrix
