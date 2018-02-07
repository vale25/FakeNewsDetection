#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
import re
import twitter
from pymongo import MongoClient
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from Variables import consumerKey, consumerSecret, accessToken, accessTokenSecret

api = twitter.Api(consumer_key=consumerKey,
                  consumer_secret=consumerSecret,
                  access_token_key=accessToken,
                  access_token_secret=accessTokenSecret)

'''
def replace_trash(unicode_string):
    for i in range(0, len(unicode_string)):
        try:
            unicode_string[i].encode("ascii")
        except:
            # means it's non-ASCII
            unicode_string = unicode_string.replace(unicode_string[i], " ")  # replacing it with a single space
    return unicode_string

user = api.GetUser("326830914").__getattribute__("description")
print user
text = replace_trash(user)
print text
'''

client = language.LanguageServiceClient()
mongo_client = MongoClient('localhost:27017')

database = mongo_client['twitter']
collection = database['tweets']
record = collection.find({"Tweet.user.description": {"$regex": ".+"}})


descriptions = {}
for doc in record:
    tweet = doc["Tweet"]
    user = tweet["user"]
    user_id = user["id"]
    desc = user["description"]
    descriptions[user_id] = desc

i = 0
with open("/media/valentina/Data/tesi/sentiment_analysis.txt", "w") as file:
    for k,v in descriptions.items():
        try:
            document = types.Document(content=v, type=enums.Document.Type.PLAIN_TEXT)
            annotations = client.analyze_sentiment(document=document)
            score = annotations.document_sentiment.score
            magnitude = annotations.document_sentiment.magnitude
            file.write(str(k) + "," + str(score) + "," + str(magnitude) + "\n")
        except:
            print "errore"
        print i
        i+=1
file.close()

