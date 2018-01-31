#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys


import tagme, ast
from unidecode import unidecode
import numpy, time
from itertools import islice
from Variables import tagme_token, trainset_senza_duplicati

reload(sys)
sys.setdefaultencoding('utf8')

tagme.GCUBE_TOKEN = tagme_token


# questa classe prende per ogni notizia le annotazioni trovate da Tagme con score >= 0.3,
# ne calcola la similarità le une con le altre, poi calcola separatamente la similarità totale
# delle fake e quella delle real per vedere quale dei due pool presenta la similarità
# interna più elevata


def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

mean_list_fake, mean_list_real = [], []

num_line = 1

def compute_mean(text, list):

    ann_dict = {}
    annotations = tagme.annotate(text)
    # print(annotations.get_annotations())
    for ann in annotations.get_annotations(0.3):
        ann_dict[ann.entity_id] = ann.score
        # print ann
    # print "------------"
    final_ann = []

    if len(ann_dict) > 1:
        if len(ann_dict) > 10:
            ordered = sorted(ann_dict.items(), key=lambda x: x[1], reverse=True)
            top_ann = ordered[:10]
            final_ann = [x[0] for x in top_ann]
        else:
            final_ann = [x for x in ann_dict]
        media_temp = []
        for i in range(len(final_ann)):
            interest = final_ann[i]
            for j in range(i + 1, len(final_ann)):
                keyword = final_ann[j]
                if interest != keyword:
                    rels = tagme.relatedness_wid((interest, keyword))
                    #print "relatedness is:"
                    #print rels.relatedness[0].rel
                    media_temp.append(rels.relatedness[0].rel)
        media = numpy.mean(media_temp)
        list.append(media)
        print media
    else:
        print "solo un'annotazione trovata per il testo"



with open(trainset_senza_duplicati, "r") as dataset:

    # inserisce le prime n righe nella lista head per poter fare test su un dataset ristretto
    '''n = 500
    x = 0
    head = list(islice(realset, n))
    for line in head:
        x+=1
        if (x>330):'''

    for line in dataset:

        #line = realset.readline()
            article = ast.literal_eval(line)
            text = article['text']
            print num_line
            #print text[:50]
            if article['label'] == "REAL":
                try:
                    compute_mean(text, mean_list_real)
                except:
                    print "-----------ERROR---------------"
            else:
                try:
                    compute_mean(text, mean_list_fake)
                except:
                    print "-----------ERROR---------------"
            num_line+=1

dataset.close

total_mean_fake = numpy.mean(mean_list_fake)
total_mean_real = numpy.mean(mean_list_real)

print ("total mean real: %f" %total_mean_real)
print ("total mean fake: %f" %total_mean_fake)

output = open("means.txt", "wb")
output.write("total mean real: %f" %total_mean_real)
output.write("\n")
output.write("total mean fake: %f" %total_mean_fake)
output.close()