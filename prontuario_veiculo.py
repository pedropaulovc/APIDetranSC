#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 2, 2012

@author: pedropaulovc
'''

from BeautifulSoup.BeautifulSoup import BeautifulSoup
import re
from copy import deepcopy

class ProntuarioVeiculo(object):
    '''
    classdocs
    '''

    def __init__(self, prontuario_html):
        '''
        Constructor
        '''
        
        self.__soup = \
            BeautifulSoup(prontuario_html, fromEncoding='iso-8859-1', 
                          convertEntities=BeautifulSoup.HTML_ENTITIES)
        self.__prontuario = {}
        
        self._parsear_dados_veiculo()
        self._parsear_debitos()
        self._parsear_infracoes_em_autuacao()
        self._parsear_listagem_multas()
        self._parsear_historico_multas()
        self._parsear_ultimo_processo()
        self._parsear_recurso_infracao()
    
    def obter_prontuario(self):
        return deepcopy(self.__prontuario)
            
    def _parsear_dados_veiculo(self):
        tabela = self.__soup.find('div', id='div_servicos_02' ).table.tbody
        
        for celula in tabela.findAll('td'):
            dado = celula.findAll(text=True)
            if len(dado) == 2:
                self.__prontuario[dado[0].strip()] = dado[1].strip()
        
    def _parsear_debitos(self):
        tabela = self.__soup.find('div', id='div_servicos_03' ).table.tbody
        
        debitos = []
        for linha in tabela.findAll('tr')[1:-1]:
            debito = {}
            
            texto = linha.td.findAll(text=True) 
            if texto == None:
                texto = ''
            debito[u'Classe'] = ''.join(texto).strip()
            
            link = ''
            if linha.td.a != None:
                link = linha.td.a['href'].strip()
            debito[u'Link'] = link
            
            celulas = [u'Número DetranNet', u'Vencimento', u'Valor Nominal(R$)',
                        u'Multa(R$)', u'Juros(R$)', u'Valor Atual(R$)']
            for celula, valor in zip(celulas, linha.findAll('td')[1:]):
                debito[celula] = valor.string.strip()
            
            debitos.append(debito)
        
        self.__prontuario[u'Débitos'] = debitos

    def _parsear_infracoes_em_autuacao(self):
        tabela = self.__soup.find('div', id='div_servicos_10' ).table.tbody
        
        celula_filha = lambda tag: tag.name == 'td' and tag.table == None
        celulas = tabela.findAll(celula_filha)[3:]
        
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
    def _parsear_listagem_multas(self):
        tabela = self.__soup.find('div', id='div_servicos_04' ).table.tbody
        
        if tabela.tr.td.find(text=re.compile(u'Nenhuma?')):
            self.__prontuario[u'Listagem de Multas'] = []
            return

    def _parsear_historico_multas(self):
        tabela = self.__soup.find('div', id='div_servicos_07' ).table.tbody
        
        celula_filha = lambda tag: tag.name == 'td' and tag.table == None
        celulas = tabela.findAll(celula_filha)[3:]
        
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

    def _parsear_ultimo_processo(self):
        tabela = self.__soup.find('div', id='div_servicos_11' ).table.tbody
        
        ultimo_processo = {}
        celulas = tabela.findAll('td')
        for celula in celulas[:5]:
            dado = celula.findAll(text=True)
            ultimo_processo[dado[0]] = dado[1]
        for i in range(7, len(celulas), 2):
            chave = celulas[i].findAll(text=True)[0]
            valor = celulas[i + 1].findAll(text=True)[0]
            ultimo_processo[chave] = valor
            
        self.__prontuario[u'Último Processo'] = ultimo_processo

    #TODO: Implementar
    def _parsear_recurso_infracao(self):
        tabela = self.__soup.find('div', id='div_servicos_09' ).table.tbody
        
        if tabela.tr.td.find(text=re.compile(u'Nenhuma?')):
            self.__prontuario[u'Recurso de Infração'] = []
            return

if __name__ == '__main__':
    prontuario = ProntuarioVeiculo(open('../../tmp/prontuarioVeiculo.html').read())
    for k, v in prontuario.obter_prontuario().items():
        print str(k) + ': ' + str(v)
