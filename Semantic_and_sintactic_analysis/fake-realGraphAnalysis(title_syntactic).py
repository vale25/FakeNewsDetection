#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import ast
import math
import re
from collections import Counter

import GraphCreator
from Variables import *

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

def ListFromDict(dict) :
    list = []
    for key, value in dict:
        list.append(value)
    return list

fake = "Nothing Good Can Come of This Election??and That?s Good".replace('\n', '')
fake2 = "List of Republicans opposing Trump | OffGuardian".replace('\n', '')
fake3 = "Putin: Use of 'mythical' Russian military threat a ?profitable business'".replace('\n', '')
fake4 = "Will the Media Reset After the Election or Are We Stuck With This Tabloid Stuff?".replace('\n', '')
fake5 = "DOJ COMPLAINT: Comey Under Fire Over Partisan Witch Hunt For Hillary (TWEETS/VIDEO)".replace('\n', '')
fake6 = "BREAKING : Hillary Campaign Manager Deletes his Entire Twitter Timeline ? TruthFeed".replace('\n', '')
fake7 = "Assange claims ?crazed? Clinton campaign tried to hack WikiLeaks".replace('\n', '')
fake8 = "The ?P? in PBS Should Stand for ?Plutocratic? or ?Pentagon?".replace('\n', '')
fake9 = "Anti-Trump Protesters Are Tools of the Oligarchy     : Information".replace('\n', '')
fake10 = "Biden and Trump Agree to Fight Pistol Duel--Final Arrangements Pending".replace('\n', '')

real = "Why Ted Cruz Has the Most to Lose in New Hampshire".replace('\n', '')
real2 = "Bernie Sanders says private meeting with Pope Francis is not an endorsement".replace('\n', '')
real3 = "Alabama Lawmaker: Same-Sex Couples Don?t Deserve Same Financial Benefits As Other Families".replace('\n', '')
real4 = "GOP Senator David Perdue Jokes About Praying for Obama?s Death".replace('\n', '')
real5 = "State Department says it can't find emails from Clinton IT specialist".replace('\n', '')
real6 = "In Ethiopia, Obama seeks progress on peace, security in East Africa".replace('\n', '')
real7 = "ISIS claims responsibility for Garland, Texas, shooting".replace('\n', '')
real8 = "The ?blame the left? crew: What the right?s new Hebdo attack is really about".replace('\n', '')
real9 = "Police Arrest Suspect In Charleston Church Shooting".replace('\n', '')
real10 = "Donald Trump?s collapse was caused by one big factor: Hillary Clinton".replace('\n', '')


'''vector1 = text_to_vector(real)
vector2 = text_to_vector(real2)
vector3 = text_to_vector(real3)
vector4 = text_to_vector(real4)
vector5 = text_to_vector(real5)
vector6 = text_to_vector(real6)
vector7 = text_to_vector(real7)
vector8 = text_to_vector(real8)
vector9 = text_to_vector(real9)
vector10 = text_to_vector(real10)'''

vector1 = text_to_vector(fake)
vector2 = text_to_vector(fake2)
vector3 = text_to_vector(fake3)
vector4 = text_to_vector(fake4)
vector5 = text_to_vector(fake5)
vector6 = text_to_vector(fake6)
vector7 = text_to_vector(fake7)
vector8 = text_to_vector(fake8)
vector9 = text_to_vector(fake9)
vector10 = text_to_vector(fake10)

def cosineSim(vector1):
    with open(Fake_dataset_GraphAnalysis,'r') as dataset:
        conta = 0
        for line in dataset:
            article = ast.literal_eval(line)
            text2 = article['title']
            vector2 = text_to_vector(text2)
            cosine = get_cosine(vector1, vector2)
            cosineSimDict[conta] = cosine
            conta+=1
            print 'Cosine:', cosine

        SortedDict = sorted(cosineSimDict.items(), key=lambda x: x[1])
        SortedDict.reverse()

    return SortedDict


dict1 = cosineSim(vector1)
print(dict1)
list1 = ListFromDict(dict1)
dict2 = cosineSim(vector2)
list2 = ListFromDict(dict2)
dict3 = cosineSim(vector3)
list3 = ListFromDict(dict3)
dict4 = cosineSim(vector4)
list4 = ListFromDict(dict4)
dict5 = cosineSim(vector5)
list5 = ListFromDict(dict5)
dict6 = cosineSim(vector6)
list6 = ListFromDict(dict6)
dict7 = cosineSim(vector7)
list7 = ListFromDict(dict7)
dict8 = cosineSim(vector8)
list8 = ListFromDict(dict8)
dict9 = cosineSim(vector9)
list9 = ListFromDict(dict9)
dict10 = cosineSim(vector10)
list10 = ListFromDict(dict10)

#Salva la notizia con valore di coseno similarita' piu' alto e più basso e ritrovale nel dataset.
#I DATASET FAKE O REAL PASSATI IN QUESTO PUNTO SONO STATI RIPULITI DELLE NOTIZIE O CON CAMPO TEXT VUOTO OPPURE CON TEXT NON SIGNIFICATIVO (CONTENENTE AD ESEMPIO SOLO UNA O DUE PAROLE) PER EVITARE UNA PERDITA DI EFFICACIA NEL CALCOLO DELLA SIMILARITA'
def FindMinMaxSimText(dict):
    contatore = 0
    contatore2 = 0
    maxSim = dict[0][0]
    dict.reverse()
    minSim = dict[0][0]
    with open(Fake_dataset_GraphAnalysis,'r') as dataset:
        for line in dataset:
            if contatore == minSim:
                article = ast.literal_eval(line)
                NewsWithMinSim = article['title'].replace('\n', '')
            contatore+=1
            if contatore2 == maxSim:
                article = ast.literal_eval(line)
                NewsWithMaxSim = article['title'].replace('\n', '')
            contatore2+=1

    print("News con similarita' minima rispetto alla news inserita: \n")
    print(NewsWithMinSim)

    print("\n News con similarita' massima rispetto alla news inserita: \n")
    print(NewsWithMaxSim)
    print("\n ----------------------------------------------------------------------------------------------------------------------------------\n ")


def fakePrint():
    print("News1 inserita:\n")
    print(fake + "\n")
    FindMinMaxSimText(dict1)

    print("News2 inserita:\n")
    print(fake2 + "\n")
    FindMinMaxSimText(dict2)

    print("News3 inserita:\n")
    print(fake3 + "\n")
    FindMinMaxSimText(dict3)

    print("News4 inserita:\n")
    print(fake4 + "\n")
    FindMinMaxSimText(dict4)

    print("News5 inserita:\n")
    print(fake5 + "\n")
    FindMinMaxSimText(dict5)

    print("News6 inserita:\n")
    print(fake6 + "\n")
    FindMinMaxSimText(dict6)

    print("News7 inserita:\n")
    print(fake7 + "\n")
    FindMinMaxSimText(dict7)

    print("News8 inserita:\n")
    print(fake8 + "\n")
    FindMinMaxSimText(dict8)

    print("News9 inserita:\n")
    print(fake9 + "\n")
    FindMinMaxSimText(dict9)

    print("News10 inserita:\n")
    print(fake10 + "\n")
    FindMinMaxSimText(dict10)


def realPrint():
    print("News1 inserita:\n")
    print(real + "\n")
    FindMinMaxSimText(dict1)

    print("News2 inserita:\n")
    print(real2 + "\n")
    FindMinMaxSimText(dict2)

    print("News3 inserita:\n")
    print(real3 + "\n")
    FindMinMaxSimText(dict3)

    print("News4 inserita:\n")
    print(real4 + "\n")
    FindMinMaxSimText(dict4)

    print("News5 inserita:\n")
    print(real5 + "\n")
    FindMinMaxSimText(dict5)

    print("News6 inserita:\n")
    print(real6 + "\n")
    FindMinMaxSimText(dict6)

    print("News7 inserita:\n")
    print(real7 + "\n")
    FindMinMaxSimText(dict7)

    print("News8 inserita:\n")
    print(real8 + "\n")
    FindMinMaxSimText(dict8)

    print("News9 inserita:\n")
    print(real9 + "\n")
    FindMinMaxSimText(dict9)

    print("News10 inserita:\n")
    print(real10 + "\n")
    FindMinMaxSimText(dict10)

realPrint()

#Crea il grafo delle News
GraphCreator.createGraph(list1, list2, list3, list4, list5, list6, list7, list8, list9, list10, len(list1), 0)