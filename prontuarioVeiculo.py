#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 2, 2012

@author: pedropaulovc
'''

from BeautifulSoup.BeautifulSoup import BeautifulSoup
import re

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
        tabela = self.__soup.find("div", id="div_servicos_10" ).table.tbody
        
        celulaFilha = lambda tag: tag.name == 'td' and tag.table == None
        celulas = tabela.findAll(celulaFilha)[3:]
        
        infracoes = []
        for i in range(len(celulas)/7):
            linha = 7 * i
            
            infracao = {}
            infracao[u'Número'] = celulas[linha].a.string
            infracao[u'Link'] = celulas[linha].a['href'].strip()
            infracao[u'Valor'] = celulas[linha + 1].string.strip()
            infracao[u'Situação'] = celulas[linha + 2].string.strip()
            infracao[u'Descrição 1'] = celulas[linha + 3].string.strip()
            infracao[u'Descrição 2'] = celulas[linha + 4].string.strip()
            infracao[u'Local/Complemento 1'] = celulas[linha + 5].string.strip()
            infracao[u'Local/Complemento 2'] = celulas[linha + 6].string
            if infracao[u'Local/Complemento 2'] == None:
                infracao[u'Local/Complemento 2'] = u''
            infracao[u'Local/Complemento 2'] = infracao[u'Local/Complemento 2'].strip()
            
            infracoes.append(infracao)
            
        self.__prontuario[u'Infrações em Autuação'] = infracoes

    #TODO: Implementar
    def __parsearListagemMultas(self):
        tabela = self.__soup.find("div", id="div_servicos_04" ).table.tbody
        
        if tabela.tr.td.find(text=re.compile(u'Nenhuma?')):
            self.__prontuario[u'Listagem de Multas'] = []
            return

    def __parsearHistoricoMultas(self):
        tabela = self.__soup.find("div", id="div_servicos_07" ).table.tbody
        
        celulaFilha = lambda tag: tag.name == 'td' and tag.table == None
        celulas = tabela.findAll(celulaFilha)[3:]
        
        multas = []
        for i in range(len(celulas)/7):
            linha = 7 * i
            
            multa = {}
            multa[u'Número'] = celulas[linha].a.string
            multa[u'Link'] = celulas[linha].a['href'].strip()
            multa[u'Lançamento'] = celulas[linha + 1].string.strip()
            multa[u'Pagamento'] = celulas[linha + 2].string.strip()
            multa[u'Descrição 1'] = celulas[linha + 3].string.strip()
            multa[u'Descrição 2'] = celulas[linha + 4].string.strip()
            multa[u'Local/Complemento 1'] = celulas[linha + 5].string.strip()
            multa[u'Local/Complemento 2'] = celulas[linha + 6].string
            if multa[u'Local/Complemento 2'] == None:
                multa[u'Local/Complemento 2'] = u''
            multa[u'Local/Complemento 2'] = multa[u'Local/Complemento 2'].strip()
            
            multas.append(multa)
            
        self.__prontuario[u'Histórico de Multas'] = multas

    def __parsearUltimoProcesso(self):
        tabela = self.__soup.find("div", id="div_servicos_11" ).table.tbody
        
        ultimoProcesso = {}
        celulas = tabela.findAll('td')
        for celula in celulas[:5]:
            dado = celula.findAll(text=True)
            ultimoProcesso[dado[0]] = dado[1]
        for i in range(7, len(celulas), 2):
            chave = celulas[i].findAll(text=True)[0]
            valor = celulas[i + 1].findAll(text=True)[0]
            ultimoProcesso[chave] = valor
            
        self.__prontuario[u'Último Processo'] = ultimoProcesso

    #TODO: Implementar
    def __parsearRecursoInfracao(self):
        tabela = self.__soup.find("div", id="div_servicos_09" ).table.tbody
        
        if tabela.tr.td.find(text=re.compile(u'Nenhuma?')):
            self.__prontuario[u'Recurso de Infração'] = []
            return

    def obterDado(self, dado):
        return self.__prontuario[dado]
    
    def obterDadosDisponiveis(self):
        return self.__prontuario.keys()
    
    def imprimirDadosDisponiveis(self):
        for c, v in self.__prontuario.items():
            print str(c) + ": " + str(v)
            

if __name__ == '__main__':
    prontuario = ProntuarioVeiculo(open("../../tmp/prontuarioVeiculo.html").read())
    prontuario.imprimirDadosDisponiveis()
