#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# questa classe individua attraverso Tagme gli argomenti più rilevanti per i due pool di notizie
# real e fake per farne un confronto
# Fare lo stesso anche per i soli titoli


import os, sys
import tagme, ast
from unidecode import unidecode
import numpy, time
from itertools import islice
from Variables import tagme_token, real_news_json, fake_news_json
from requests.exceptions import Timeout, ConnectionError

reload(sys)
sys.setdefaultencoding('utf8')

tagme.GCUBE_TOKEN = tagme_token


topics_real, topics_fake = {}, {}
values_real, values_fake = {}, {}


def retrieveTopics(text, topics):
    try:
        annotations = tagme.annotate(text)
        for ann in annotations.get_annotations(0.3):
            topics.setdefault(ann.entity_title, []).append(ann.score)
    except (Timeout, ConnectionError) as exc:
        print "errore di connessione"


def computeValue(topics, values):
    keys = topics.keys()
    for k in keys:
        scores = topics[k]
        mean = numpy.mean(scores)*len(scores)
        values[k] = mean

'''i=1
with open(real_news_json, "r") as real:

    #n = 10
    #head = list(islice(real, n))
    #for line in head:

    for line in real:
        article = ast.literal_eval(line)
        text = article['text']
        retrieveTopics(text, topics_real)
        print i
        i+=1
real.close

computeValue(topics_real, values_real)
topics_real_sorted = sorted(values_real.items(), key=lambda x: x[1], reverse=True)
top100_real = topics_real_sorted[:100]

print "scrivo su file..."

with open("top100_real", "w") as top:

    for elem in top100_real:
        top.write(str(elem[0])+" "+str(elem[1])+"\n")
top.close

print "primo file scritto" '''

j=1
with open(fake_news_json, "r") as fake:
    for line in fake:
        article = ast.literal_eval(line)
        text = article['text']
        retrieveTopics(text, topics_fake)
        print j
        j+=1
fake.close

computeValue(topics_fake, values_fake)
topics_fake_sorted = sorted(values_fake.items(), key=lambda x: x[1], reverse=True)
top100_fake = topics_fake_sorted[:100]

print "scrivo su file..."

with open("top100_fake", "w") as top2:

    for elem in top100_fake:
        top2.write(str(elem[0])+" "+str(elem[1])+"\n")
top2.close

print "secondo file scritto"


