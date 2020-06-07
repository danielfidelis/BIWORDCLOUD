#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from wordcloud import WordCloud
from PIL import Image
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk

def ler_arquivo(arquivo):
    with open(arquivo, mode='r') as txt_file:
        dados = txt_file.readlines()
    dados = [item.replace('\n','') for item in dados]
    conjunto_dados = set(dados)
    
    return conjunto_dados


def gerar_nuvem(texto):
    maskArray = np.array(Image.open("cloud.png"))
    wordcloud = WordCloud(collocations=False, background_color = "white", max_words = 300, mask = maskArray)
    #wordcloud = WordCloud(regexp="\w[\w_]+", collocations=False, width=800, height=600, max_words=20)
    wordcloud.generate(texto)
    
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def ler_dados(arquivo):
    dados = pd.read_csv(arquivo, sep=';', encoding='utf-8')
    return dados

   
def obter_campo(dados, campo):
    return dados[campo]    


def palavra_valida(palavra, minha_stopwords):
    if palavra not in nltk.corpus.stopwords.words('portuguese') and palavra.isalpha() and palavra not in minha_stopwords:
        return True
    
    return False


def processar(dados, minhas_stopwords):
    texto = dados.str.cat(sep=' ')
    tokens = nltk.word_tokenize(texto, language='portuguese')

    texto_limpo = []
    for palavra in tokens:
        if palavra_valida(palavra.lower(), minhas_stopwords):
            texto_limpo.append(palavra)
    
    texto_processado = pd.Series(texto_limpo).str.cat(sep=' ')
    return texto_processado



''' Main program '''
def main():
    
    minhas_stopwords = ler_arquivo("minhas_stopwords.txt")
    dados = ler_dados("reclamacoes.csv")
    conteudo = obter_campo(dados, 'serviço')

    texto = processar(conteudo, minhas_stopwords)
    gerar_nuvem(texto)
    
    del dados
    del texto
    
    
    
    
    

if __name__ == "__main__":
    sys.exit(main())