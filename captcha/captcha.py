# -*- coding: utf-8 -*-
'''
Created on Jan 2, 2012

@author: pedropaulovc
'''

from comparador_vetor import ComparadorVetor
import Image
import hashlib
import os

class Captcha(object):
    '''
    classdocs
    '''

    def __init__(self, dir_letras='./letras/'):
        '''
        Constructor
        '''
        self._dir_letras = dir_letras
        self._treino = None
    
    def treinar(self, caminho_imagem, solucao):
        imagem = Image.open(caminho_imagem)
        imagem = imagem.convert('P')
        imagem = self._gerar_imagem_preto_branco(imagem)
        pos_letras = self._localizar_letras(imagem)
        self._salvar_treino(imagem, pos_letras, solucao)
    
    def resolver(self, caminho_desafio):
        desafio = Image.open(caminho_desafio)
        desafio = desafio.convert('P')
        desafio = self._gerar_imagem_preto_branco(desafio)
        pos_letras_desafio = self._localizar_letras(desafio)

        resposta = ''
        confianca = 1.0
        for pos_letra in pos_letras_desafio:
            letra = desafio.crop((pos_letra[0] , 0, pos_letra[1], desafio.size[1]))
            
            chutes = self._calcular_chutes(letra)
            
            resposta = '%s%s' % (resposta, chutes[0][1])
            confianca *= chutes[0][0]
            
        return (confianca, resposta)
    
    def _gerar_imagem_preto_branco(self, imagem):
        imagem_pb = Image.new('P', imagem.size, 255)
        
        cores = imagem.getcolors()
        cor_letra = cores[1][1]
        if cores[0][0] < cores[1][0]:
            cor_letra = cores[0][1]
            
        for x in range(imagem.size[1]):
            for y in range(imagem.size[0]):
                pix = imagem.getpixel((y, x))
                if pix == cor_letra:
                    imagem_pb.putpixel((y, x), 0)
        
        return imagem_pb
    
    def _localizar_letras(self, imagem):
        na_letra = False
        encontrou_letra = False
        inicio = 0
        fim = 0
        
        letras = []
        
        for y in range(imagem.size[0]): # fatiar horizonta;
            for x in range(imagem.size[1]): # fatiar vertical
                pix = imagem.getpixel((y, x))
                if pix != 255:
                    na_letra = True
        
            if encontrou_letra == False and na_letra == True:
                encontrou_letra = True
                inicio = y
        
            if encontrou_letra == True and na_letra == False:
                encontrou_letra = False
                fim = y
                letras.append((inicio, fim))
            na_letra = False
            
        return letras
    
    def _salvar_treino(self, imagem, letras, solucao):
        for i in range(len(solucao)):
            m = hashlib.md5()
            imagem_letra = imagem.crop((letras[i][0] , 0, letras[i][1], imagem.size[1]))
            m.update(imagem_letra.tostring())
            diretorio_letra = '%s%s/' % (self._dir_letras, solucao[i])
            if not os.path.exists(diretorio_letra):
                os.mkdir(diretorio_letra)
            imagem_letra.save('%s%s.gif' % (diretorio_letra, m.hexdigest()))

    def _montar_vetor_imagem(self, imagem):
        vetor_imagem = {}
    
        cont = 0
        for i in imagem.getdata():
            vetor_imagem[cont] = i
            cont += 1
    
        return vetor_imagem
    
    def _carregar_treino(self):
        imagens = []
        letras = os.listdir(self._dir_letras)
        
        for letra in letras:
            dir_letra = '%s%s/' % (self._dir_letras, letra)
            for img in os.listdir(dir_letra):
                imagem_letra = Image.open('%s%s' % (dir_letra, img))

                vetor_letra = []
                vetor_letra.append(self._montar_vetor_imagem(imagem_letra))
                
                imagens.append({letra:vetor_letra})
        
        return imagens

    def _calcular_chutes(self, letra):
        comp = ComparadorVetor()
        chutes = []
    
        if(self._treino == None):
            self._treino = self._carregar_treino()
    
        for imagem in self._treino:
            for x, y in imagem.iteritems():
                if len(y) != 0:
                    relacao = comp.relacao(y[0], self._montar_vetor_imagem(letra))
                    chutes.append((relacao, x))

        return chutes.sort(reverse=True)
    
if __name__ == '__main__':
    captcha = Captcha()
    for arquivo in os.listdir('./treino'):
        captcha.treinar('./treino/' + arquivo, arquivo[:-4])
    for desafio in os.listdir('./desafios'):
        resposta = captcha.resolver('./desafios/' + desafio)      
        print resposta,
        if resposta[1] == desafio[:-4]:
            print 'SUCESSO'
        else:
            print 'FRACASSO:' + desafio 

