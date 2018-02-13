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


def sentiment_analysis():

    record = collection.find({"Tweet.user.description": {"$regex": ".+"}})
    descriptions = {}
    for doc in record:
        tweet = doc["Tweet"]
        user = tweet["user"]
        user_id = user["id"]
        desc = user["description"]
        descriptions[user_id] = desc



    '''final_desc = {}
    for x in dict_active_users:
        if descriptions.has_key(x):
            final_desc[x] = descriptions[x]
    
    print "utenti attivi con bio:"
    print len(final_desc)
    print final_desc'''

    # GLI UTENTI CHE HANNO LETTO ALMENO 10 NEWS E HANNO LA BIO SONO 992 SU 1159


    i = 0
    with open("/media/valentina/Data/tesi/sentiment_analysis.txt", "w") as file:
        for elem in record_news:
            tweet = elem["Tweet"]
            user = tweet["user"]
            id = user["id"]
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
            print i
            i+=1
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


sentiment_analysis()