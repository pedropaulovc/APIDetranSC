#!/usr/bin/python
# -*- coding: utf-8 -*-
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
            BeautifulSoup(prontuarioHTML, fromEncoding="iso-8859-1", 
                          convertEntities=BeautifulSoup.HTML_ENTITIES)
        self.__prontuario = {}
        
        self.__parsearDadosVeiculo()
        self.__parsearDebitos()
        self.__parsearInfracoesEmAutuacao()
        self.__parsearListagemMultas()
        self.__parsearHistoricoMultas()
        self.__parsearUltimoProcesso()
        self.__parsearRecursoInfracao()
        

    def __parsearDadosVeiculo(self):
        tabela = self.__soup.find("div", id="div_servicos_02" ).table.tbody
        
        for celula in tabela.findAll('td'):
            dado = celula.findAll(text=True)
            if len(dado) == 2:
                self.__prontuario[dado[0].strip()] = dado[1].strip()
        
    def __parsearDebitos(self):
        tabela = self.__soup.find("div", id="div_servicos_03" ).table.tbody
        
        debitos = []
        for linha in tabela.findAll('tr')[1:-1]:
            debito = {}
            
            texto = linha.td.findAll(text=True) 
            if texto == None:
                texto = ""
            debito[u'Classe'] = ''.join(texto).strip()
            
            link = ""
            if linha.td.a != None:
                link = linha.td.a['href'].strip()
            debito[u'Link'] = link
            
            celulas = [u'Número DetranNet', u'Vencimento', u'Valor Nominal(R$)',
                        u'Multa(R$)', u'Juros(R$)', u'Valor Atual(R$)']
            for celula, valor in zip(celulas, linha.findAll('td')[1:]):
                debito[celula] = valor.string.strip()
            
            debitos.append(debito)
        
        self.__prontuario[u'Débitos'] = debitos

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
    
    def imprimirDadosDisponiveis(self):
        for c, v in self.__prontuario.items():
            print str(c) + ": " + str(v)
        for debito in self.__prontuario[u'Débitos']:
            print debito

if __name__ == '__main__':
    prontuario = ProntuarioVeiculo(open("../../tmp/prontuarioVeiculo.html").read())
    prontuario.imprimirDadosDisponiveis()
