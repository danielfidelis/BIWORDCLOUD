#!/usr/bin/env python3

from wordcloud import WordCloud
from PIL import Image
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk
import operator


def ler_arquivo(arquivo):
    with open(arquivo, mode='r') as txt_file:
        dados = txt_file.readlines()
    dados = [item.replace('\n','') for item in dados]
    conjunto_dados = set(dados)
    
    return conjunto_dados


def gerar_nuvem(texto):
    maskArray = np.array(Image.open("cloud.png"))
    wordcloud = WordCloud(collocations=False, background_color = "white", max_words = 300, mask = maskArray)

    texto_arr = texto.split()

    for index, nome in enumerate(texto_arr):
        texto_arr[index] = nome.replace("Î", " ")

    freq_dict = dict.fromkeys(texto_arr)

    for e in freq_dict:
        freq_dict[e] = texto_arr.count(e)
    
    maximo = max(freq_dict.items(), key=operator.itemgetter(1))[1]

    for e in freq_dict:
        freq_dict[e] = freq_dict[e] / maximo

    wordcloud.generate_from_frequencies(freq_dict)
    
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def ler_dados(arquivo):
    dados = pd.read_csv(arquivo, sep=';', encoding='latin-1')
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


"""
Aglutina as palavras que compõe o nome de cada empresa em uma única,
utilizando um caractére especial, que posteriormente será removido no
momento da geração da nuvem de palavras.
"""
def fix_subsidiarias(dados):
    for index, row in dados.iterrows():
        if row['subsidiaria'] == 'NULL' or row['subsidiaria'] == None or pd.isna(row['subsidiaria']):
            if not pd.isna(row['empresa']):
                emp = row['empresa']
                row['subsidiaria'] = emp.strip().replace(" ", "Î")
        else:
            sub = row['subsidiaria']
            sub = sub.split("/")[0].strip()
            row['subsidiaria'] = sub.replace(" ", "Î")
    return dados


''' 
Executa o programa. A variável 'tipo_nuvem' deve receber uma string
correspondente a uma das colunas do arquivo de entrada.
'''
def main():
    tipo_nuvem = 'subsidiaria'
    minhas_stopwords = ler_arquivo("minhas_stopwords.txt")
    dados = ler_dados("reclamacoes.csv")

    if tipo_nuvem == 'subsidiaria':
        dados = fix_subsidiarias(dados)
    
    conteudo = obter_campo(dados, tipo_nuvem)

    texto = processar(conteudo, minhas_stopwords)
    gerar_nuvem(texto)
    
    del dados
    del texto
    
if __name__ == "__main__":
    sys.exit(main())