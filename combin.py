#!/usr/bin/env python3

import math
import sys

class Combinations:
    """Classe que lida com os cálculos de número de combinações"""

    def __init__(self, elementos, conjuntos):

        # Inicia as variáveis na classe:
        self._elementos = elementos
        self._conjuntos = conjuntos
        assert self._elementos >= self._conjuntos

    @property
    def calcComb(self):
        """Função que retorna o número de combinações para dois valores passados a função"""

        self._myComb = math.factorial(self._elementos)/(math.factorial(self._conjuntos)*math.factorial
                                        (self._elementos-self._conjuntos))
        return self._myComb

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Calculando combinações de 6, 4:')
        myComb = Combinations(6, 4).calcComb
        print(myComb)
    elif len(sys.argv) == 3 and sys.argv[1].isnumeric() and sys.argv[2].isnumeric():
        print('Calculando combinações de %s, %s:' %(sys.argv[1], sys.argv[2]))
        myComb = Combinations(int(sys.argv[1]), int(sys.argv[2])).calcComb
        print(myComb)
    else:
        print('Parâmetros inválidos')