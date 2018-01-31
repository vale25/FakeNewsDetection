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
with open(RealJson_notiziaAggiunta,'r') as dataset:
    for line in dataset:
        if cont != 10:
            article = ast.literal_eval(line)
            text = article['text'].replace('\n', '')
            docs.append(nlp(unicode(text, errors='replace')))
            print(cont)
            cont+=1
print(docs)

for doc in docs:
    fakenews = nlp(u"Politics Former British Prime Minister Tony Blair says UK voters ?have to build the capability to mobilize and to organize? against Brexit. \nFormer British Prime Minister Tony Blair says Britain should keep its ?options open? on whether or not to leave the European Union until after Brexit talks with the bloc are completed. \nDuring an interview on Friday with BBC Radio 4's ?Today? program, Blair described the EU referendum as ?a catastrophe? and said UK voters should be given the option of a second EU referendum. \nBritain should not withdraw from the EU until it becomes clearer how Brexit would impact UK?s economic, social and cultural future, Blair said. \n\"The bizarre thing about this referendum is that we took a decision but we still don't know the precise terms,? he said. ?There?s got to be some way, either through parliament, or through an election, possibly through another referendum, that people express their view.? \nThe former premier, who was in office from 1997 until 2007, said it should be possible for the public to switch their verdict if it becomes clear the alternative negotiated by Prime Minister Theresa May is going to be worse. \nBlair?s argument contrasts sharply with that of May, who has repeatedly said that ?Brexit means Brexit? and that she?ll respect the referendum result. Blair had argued that Britain should stay in the EU before the referendum. \nEconomic growth in the UK is expected to slow significantly next year, due to uncertainty over of the Brexit vote. \nExperts have warned that leaving the EU will severely hurt London?s position as a financial hub, unless the UK decides to keep its access to the single EU market by loosening its stance on immigration. \nIf the UK loses its access to the EU?s single market, the resulting increase in the costs of doing business and exporting to the EU would hurt Britain?s competitive position in Europe. Loading ...")
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
with open(RealJson_notiziaAggiunta, 'r') as dataset:
    for line in dataset:
        if contatore2 == maxSim:
            article = ast.literal_eval(line)
            lineTextReal = article['text'].replace('\n', '')
        contatore2+=1
print("Fake news inserita: \n")
print(str(fakenews))
print("\n Real news corrispondente: \n")
print(lineTextReal)