'''
Created on Jan 2, 2012

@author: pedropaulovc
'''

from BeautifulSoup.BeautifulSoup import BeautifulSoup


class ProntuarioVeiculo(object):
    '''
    classdocs
    '''


    def __init__(self, prontuarioHTML):
        '''
        Constructor
        '''
        
        self.__soup = \
            BeautifulSoup(prontuarioHTML, fromEncoding="iso-8859-1")
        self.__prontuario = {}
        
        self.__parsearDadosVeiculo()
        self.__parsearDebitos()
        self.__parsearInfracoesEmAutuacao()
        self.__parsearListagemMultas()
        self.__parsearHistoricoMultas()
        self.__parsearUltimoProcesso()
        self.__parsearRecursoInfracao()
        

    def __parsearDadosVeiculo(self):
        dados = self.__soup.find("div", id="div_servicos_02" ).table.tbody
        
        for celula in dados.findAll('td'):
            chave = celula.contents[0]
            if chave.string == None:
                chave = ''.join(chave.findAll(text=True))
            chave = chave.strip()
            
            valor = celula.span.string
            if(valor == None):
                valor = ''.join(celula.span.findAll(text=True))            
            valor = valor.strip()
                
            self.__prontuario[chave] = valor
        
        for k, v in self.__prontuario.items():
            print str(k) + ": " + str(v)

    def __parsearDebitos(self):
        pass

    def __parsearInfracoesEmAutuacao(self):
        pass

    def __parsearListagemMultas(self):
        pass

    def __parsearHistoricoMultas(self):
        pass

    def __parsearUltimoProcesso(self):
        pass

    def __parsearRecursoInfracao(self):
        pass

    def obterDado(self, dado):
        return self.__prontuario[dado]
    
    def obterDadosDisponiveis(self):
        return self.__prontuario.keys()

if __name__ == '__main__':
    prontuario = ProntuarioVeiculo(open("../../tmp/prontuarioVeiculo.html").read())
    
