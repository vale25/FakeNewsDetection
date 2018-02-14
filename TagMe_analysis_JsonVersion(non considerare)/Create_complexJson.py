#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
import ast
from Variables import *
import json

Lucavar_real = real_news_json
Lucavar_fake = fake_news_json


newreal = open("/media/luca/Windows8_OS/Json_dataset_FakeReal_Twitter/dataset_twitter_finale/10NewsUser_real.json", "w")
newfake = open("/media/luca/Windows8_OS/Json_dataset_FakeReal_Twitter/dataset_twitter_finale/10NewsUser_fake.json", "w")

cont1 = 0
cont2 = 0
with open(Min10News_users,'r') as dataset:
    for line in dataset:
        article = ast.literal_eval(line)
        text = article["text"].encode("ascii","ignore").decode("ascii")
        url = article["url"]
        type_page = article["type_page"]
        if article['type_page'] == "Mainstream" :
            d = {"id"+str(cont1): { "url": url, "text": text, "type_page": type_page} }
            json.dump(d,newreal)
            newreal.write("\n")
            #newreal.write(line)
            cont1+=1
        else:
            d = {"id"+str(cont2) : { "url": url, "text": text, "type_page": type_page }}
            json.dump(d, newfake)
            newfake.write("\n")
            #newfake.write(line)
            cont2+=1


dataset.close()
newreal.close()
newfake.close()