'''
Created on Jan 2, 2012

@author: pedropaulovc
'''

import math

class ComparadorVetor:
    def magnitude(self, concordancia):
        total = 0
        for _, contagem in concordancia.iteritems():
            total += contagem ** 2
        return math.sqrt(total)

    def relacao(self, concordancia1, concordancia2):
        maiorValor = 0
        for palavra, contagem in concordancia1.iteritems():
            if concordancia2.has_key(palavra):
                maiorValor += contagem * concordancia2[palavra]
        return maiorValor / (self.magnitude(concordancia1) * self.magnitude(concordancia2))
