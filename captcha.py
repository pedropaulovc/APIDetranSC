'''
Created on Jan 2, 2012

@author: pedropaulovc
'''

from PIL import Image
from vectorCompare import VectorCompare
import hashlib
import os

class Captcha(object):
    '''
    classdocs
    '''

    def __init__(self, dirLetras='./letras/'):
        '''
        Constructor
        '''
        self.__dirLetras = dirLetras
    
    def treinar(self, caminhoImagem, solucao):
        try:
            imagem = Image.open(caminhoImagem)
        except:
            return
        
        imagem = imagem.convert("P")
        imagem = self.__gerarImagemPretoBranco(imagem)
        letras = self.__localizarLetras(imagem)
        self.__salvarTreino(imagem, letras, solucao)
    
    def resolver(self, caminhoDesafio):
        desafio = Image.open(caminhoDesafio)
        desafio = desafio.convert("P")
        desafio = self.__gerarImagemPretoBranco(desafio)
        posLetrasDesafio = self.__localizarLetras(desafio)

        treino = self.__carregarTreino()

        comparador = VectorCompare()        
        resposta = ""
        confianca = 1.0
        for posLetra in posLetrasDesafio:
            letra = desafio.crop((posLetra[0] , 0, posLetra[1], desafio.size[1]))
    
            chutes = []
    
            for imagem in treino:
                for x, y in imagem.iteritems():
                    if len(y) != 0:
                        chute = (comparador.relation(y[0], self.__montarVetorImagem(letra)), x)
                        chutes.append(chute)

            chutes.sort(reverse=True)
            resposta = "%s%s" % (resposta, chutes[0][1])
            confianca *= chutes[0][0]
            
        return (confianca, resposta)
    
    def __gerarImagemPretoBranco(self, imagem):
        imagemPB = Image.new("P", imagem.size, 255)
        
        cores = imagem.getcolors()
        corLetra = cores[1][1]
        if cores[0][0] < cores[1][0]:
            corLetra = cores[0][1]
            
        for x in range(imagem.size[1]):
            for y in range(imagem.size[0]):
                pix = imagem.getpixel((y, x))
                if pix == corLetra:
                    imagemPB.putpixel((y, x), 0)
        
        return imagemPB
    
    def __localizarLetras(self, imagem):
        naLetra = False
        encontrouLetra = False
        inicio = 0
        fim = 0
        
        letras = []
        
        for y in range(imagem.size[0]): # slice across
            for x in range(imagem.size[1]): # slice down
                pix = imagem.getpixel((y, x))
                if pix != 255:
                    naLetra = True
        
            if encontrouLetra == False and naLetra == True:
                encontrouLetra = True
                inicio = y
        
            if encontrouLetra == True and naLetra == False:
                encontrouLetra = False
                fim = y
                letras.append((inicio, fim))
            naLetra = False
            
        return letras
    
    def __salvarTreino(self, imagem, letras, solucao):
        for i in range(len(solucao)):
            m = hashlib.md5()
            imagemLetra = imagem.crop((letras[i][0] , 0, letras[i][1], imagem.size[1]))
            m.update(imagemLetra.tostring())
            diretorioLetra = '%s%s/' % (self.__dirLetras, solucao[i])
            if not os.path.exists(diretorioLetra):
                os.mkdir(diretorioLetra)
            imagemLetra.save("%s%s.gif" % (diretorioLetra, m.hexdigest()))

    def __montarVetorImagem(self, im):
        d1 = {}
    
        count = 0
        for i in im.getdata():
            d1[count] = i
            count += 1
    
        return d1
    
    def __carregarTreino(self):
        imagens = []
        
        letras = os.listdir(self.__dirLetras)
        
        for letra in letras:
            dirLetra = '%s%s/' % (self.__dirLetras, letra)
            for img in os.listdir(dirLetra):
                vetorLetra = []
                imagemLetra = "%s%s" % (dirLetra, img)
                vetorLetra.append(self.__montarVetorImagem(Image.open(imagemLetra)))
                imagens.append({letra:vetorLetra})
        
        return imagens

    
if __name__ == '__main__':
    captcha = Captcha()
    for arquivo in os.listdir('./treino'):
        captcha.treinar('./treino/' + arquivo, arquivo[:-4])
    print captcha.resolver('./captcha.bmp')

