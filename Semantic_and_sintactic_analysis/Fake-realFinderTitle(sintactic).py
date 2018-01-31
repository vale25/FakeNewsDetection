#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
import re, math
from collections import Counter
from Variables import *
import ast


#Questa classe calcola in maniera efficiente (circa 4 secondi)
# la realnews corrispondente ad una notizia fake inserita

conta = 0
contatore = 0
cosineSimDict = {}
WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

fakeTitle = "Biden and Trump Agree to Fight Pistol Duel--Final Arrangements Pending".replace('\n', '')

vector1 = text_to_vector(fakeTitle)
#vector2 = text_to_vector(text2)

with open(RealJson_notiziaAggiunta,'r') as dataset:
    for line in dataset:
        article = ast.literal_eval(line)
        text2 = article['title']
        vector2 = text_to_vector(text2)
        cosine = get_cosine(vector1, vector2)
        cosineSimDict[conta] = cosine
        conta+=1
        print 'Cosine:', cosine

sortedCosine = sorted(cosineSimDict.items(), key=lambda x: x[1])
sortedCosine.reverse()
print sortedCosine
#print 'Cosine:', cosine
maxSim = sortedCosine[0][0]
with open(RealJson_notiziaAggiunta,'r') as dataset:
    for line in dataset:
        if contatore == maxSim:
            article = ast.literal_eval(line)
            realnewsfindedTitle = article['title'].replace('\n', '')
            realnewsfinded = article['text'].replace('\n', '')
        contatore+=1

print("Fake news inserita: \n")
print(fakeTitle)
print("\n Real news corrispondente: \n")
print("Titolo: \n")
print(realnewsfindedTitle)
print("\n Testo \n")
print(realnewsfinded)