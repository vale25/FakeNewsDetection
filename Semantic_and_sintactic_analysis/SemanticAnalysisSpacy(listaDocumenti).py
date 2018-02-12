#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
import spacy
from Variables import *
import ast
nlp = spacy.load('en')
SemanticSimDict = {}
contatore=0

notiziaAggiunta = "/home/luca/PycharmProjects/prova_json_notizieAggiunte.json"

cont = 0
docs = []
with open(Real_dataset_GraphAnalysis,'r') as dataset:
    for line in dataset:
        #if cont != 10:
            article = ast.literal_eval(line)
            text = article['text'].replace('\n', '')
            docs.append(nlp(unicode(text, errors='replace')))
            print(cont)
            cont+=1
print(docs)

for doc in docs:
    fakenews = nlp(u"BREAKING: Trump Jumps in FL, Takes 4 Point Lead in OH \nWilliams, who has publicly stated that he was not a Trump supporter, is nevertheless a man of honor and integrity. He doesn?t sell his values to common thugs who use bylines as weapons. \nAccording to both Williams and his attorney, Jonathan Franks, Jacob Bernstein from The Times approached Williams, asking for cooperation on a story alleging that people who live in Trump-branded buildings want the Trump name removed in light of the very difficult and contentious 2016 election season. \nWilliams, an independent who lives in a Trump-developed New York building, declined to cooperate.   \nAccording to Franks, Bernstein replied to a specific request not to print Williams? address by stating he ?would be more likely to extend that courtesy if Montel gave an interview.? \nProtecting another person?s privacy, especially the privacy of the ballot box, is not a special courtesy. It?s simply common decency. \nThe Washington Examiner took their colleagues at The Times to task for this low-life journalism, noting that Williams identifies as a conservative but is not a registered Republican. He endorsed Ohio Gov. John Kasich in the 2016 GOP primary and has publicly credited Kasich for bringing him back into the conservative fold. \nPlease share this article on Facebook and Twitter to help expose the media?s liberal bias.  ")
    SemanticSimDict[contatore] = doc.similarity(fakenews)
    print(doc.similarity(fakenews))
    contatore+=1


contatore2=0
print SemanticSimDict
lineTextReal = ""
sortedSemantic = sorted(SemanticSimDict.items(), key=lambda x: x[1])
sortedSemantic.reverse()
print(sortedSemantic)
maxSim = sortedSemantic[0][0]
print(maxSim)
with open(Real_dataset_GraphAnalysis, 'r') as dataset:
    for line in dataset:
        if contatore2 == maxSim:
            article = ast.literal_eval(line)
            lineTextReal = article['text'].replace('\n', '')
        contatore2+=1
print("Fake news inserita: \n")
print(str(fakenews))
print("\n Real news corrispondente: \n")
print(lineTextReal)