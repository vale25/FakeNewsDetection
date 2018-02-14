#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
import re
import twitter
from pymongo import MongoClient
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from collections import Counter
from User_News_Twitter import activeUsers
from datetime import datetime

from Variables import consumerKey, consumerSecret, accessToken, accessTokenSecret

api = twitter.Api(consumer_key=consumerKey,
                  consumer_secret=consumerSecret,
                  access_token_key=accessToken,
                  access_token_secret=accessTokenSecret)


client = language.LanguageServiceClient()
mongo_client = MongoClient('localhost:27017')

database = mongo_client['twitter']
collection = database['tweets']


##### codice preso da User_News_Twitter

Final_dict = activeUsers()

#####
dict_active_users = Final_dict.keys()


####### prendo le news buone (1159)
news = collection.aggregate([{"$group": { "_id": "$Tweet.user.id", "id_news": { "$addToSet": "$_id"} } }])

id_news = []
for doc in news:
    id_utente = doc["_id"]
    if id_utente in dict_active_users:
        id_notizia = doc["id_news"][0]
        id_news.append(id_notizia)

record_news = collection.find({"_id": {"$in":id_news} })
#print record.count()
#######

sorted_ids = []

for elem in record_news:
    tweet = elem["Tweet"]
    user = tweet["user"]
    id = user["id"]
    sorted_ids.append(id)


def sentiment_analysis():

    record = collection.find({"Tweet.user.description": {"$regex": ".+"}})
    descriptions = {}
    for doc in record:
        tweet = doc["Tweet"]
        user = tweet["user"]
        user_id = user["id"]
        desc = user["description"]
        descriptions[user_id] = desc

    utenti = real_fake_percentage()

    final_desc = {}
    for x in utenti:
        if descriptions.has_key(x):
            final_desc[x] = descriptions[x]
    
    print "utenti attivi con bio:"
    print len(final_desc)
    #print final_desc

    # GLI UTENTI CHE HANNO LETTO ALMENO 10 NEWS E HANNO LA BIO SONO 992 SU 1159


    #i = 0
    with open("/media/valentina/Data/tesi/sentiment_analysis.txt", "w") as file:
        for id in sorted_ids:
            if id in descriptions:
                try:
                    text = descriptions[id]
                    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
                    annotations = client.analyze_sentiment(document=document)
                    score = annotations.document_sentiment.score
                    #print id, score
                    file.write("%f\n" %score)
                except:
                    print "errore"
                    file.write("%f\n" %0)
            else:
               file.write("%f\n" %0)
            #print i
            #i+=1
            print id
    file.close()


def account_age():

    today = datetime.today()
    for doc in record_news:
        tweet = doc["Tweet"]
        user = tweet["user"]
        created_at = user["createdAt"]
        date = datetime.strptime(date, '%b %d, %Y %I:%M:%S %p')
        time = today - datetime
        age = str(time.days)


def real_fake_percentage():

    real_fake = {}
    r = collection.find({ "Tweet.user.id": {"$in": dict_active_users }})
    for doc in r:
        tweet = doc["Tweet"]
        user = tweet["user"]
        id = user["id"]
        type_page = doc["type_page"]
        real_fake.setdefault(id, []).append(type_page)
    #print real_fake

    real_fake_numbers = {}
    for k in real_fake.keys():
        lista = real_fake[k]
        real, fake = 0, 0
        for elem in lista:
            if elem == "Mainstream":
                real+=1
            else:
                fake+=1
        real_fake_numbers[k] = [real, fake]
        #print real_fake_numbers[id]
    #print real_fake_numbers


    label = {}
    for elem in real_fake_numbers.keys():
        #tot = real_fake_numbers[elem][0] + real_fake_numbers[elem][1]
        #percent_real = real_fake_numbers[elem][0] *100 / tot

        # se le news real sono minori delle fake
        if real_fake_numbers[elem][0] < real_fake_numbers[elem][1]:
            label[elem] = "fake"
        else:
            label[elem] = "real"


    # prendo tutti gli utenti con label fake e li ordino per numero di news lette descrescente per prenderne i primi 1000
    utenti_fake = {}
    label_keys = label.keys()
    for u in label_keys:
        if label[u] == "fake":
            utenti_fake[u] = real_fake_numbers[u][0]+real_fake_numbers[u][1]
    utenti_buoni = sorted(utenti_fake.items(), key=lambda x: x[1], reverse=True)[:1000]


    # creo una lista con gli id di tutti gli utenti real che hanno letto almeno 5 news e i 1000 id fake estratti
    # con la funzione precedente
    utenti_final = []
    for key in label_keys:
        if label[key] == "real":
            utenti_final.append(key)
    for el in utenti_buoni:
        utenti_final.append(el[0])

    return utenti_final


    '''file = open("/media/valentina/Data/tesi/labels_5news.txt", "w")
    for elem in sorted_ids:
        print elem
        print label[elem]
        file.write(str(label[elem])+ "\n")

    file.close'''


def news_associate(news):
    utenti = real_fake_percentage()
    record = collection.find({"Tweet.user.id": {"$in": utenti}})
    for doc in record:
        tweet = doc["Tweet"]
        user = tweet["user"]
        id = user["id"]
        url = doc["url_tweet"]
        news.setdefault(id, []).append(url)
    print news
    return news

news = {}
news_associate(news)