#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
from pymongo import MongoClient
import ast
import json

mongo_client = MongoClient('localhost:27017')

database = mongo_client['twitter']
collection = database['tweets']


# da far girare sul dataset buono tweetsCleaned.json
def find_noDuplicati():
    recordreal = collection.find({"type_page": "Mainstream"})
    recordfake = collection.find({"type_page": "misinformation"})


    urlsreal = set()
    for doc in recordreal:
        url = doc["url_tweet"]
        urlsreal.add(url)

    print "news real:"
    print len(urlsreal)

    urlsfake = set()
    for doc in recordfake:
        url = doc["url_tweet"]
        urlsfake.add(url)

    print "news fake"
    print len(urlsfake)

# da far girare sul dataset grosso tweets_cleaned
def find_otherNews():
    # trova i record con url_text non buono o mancante ma che hanno url_tweet e sono misinformation
    record = collection.find({"$or": [ { "url_text": {"$regex": "utilizzando i servizi", "$options": "i"}}, {"url_text": {"$regex": "su Twitter"}}, {"url_text": {"$regex": "by using twitter", "$options": "i"}}, {"url_text": ""}, {"url_text": {"$exists": "true"}, "$where": "this.url_text.length < 1000"}, {"url_text": {"$exists": "false"}}  ], "url_tweet": {"$exists": "true"}, "type_page": "misinformation" })

    urls = set()
    id_news = []
    for doc in record:
        url = doc["url_tweet"]
        urls.add(url)
        id = doc["_id"]
        id_news.append(id)

    print "url non duplicati trovati finora:"
    print len(urls)

    url_buoni = []
    cont = 0
    with open("/media/valentina/Data/tesi/dataset_mongo/FakeNews.json", "r") as dataset:
        for line in dataset:
            article = ast.literal_eval(line)
            link = article['link']
            for u in urls:
                if link == u:
                    url_buoni.append(link)
                    cont+=1
    dataset.close
    print "link buoni da utilizzare:"
    print cont

    file = open("/media/valentina/Data/tesi/urls.txt", "w")

    for element in url_buoni:
        file.write("\""+element+"\""+",")
    file.close()

    nuovo = open("/media/valentina/Data/tesi/nuovo.json", "w")

    with open("/media/valentina/Data/tesi/tweets_cleaned.json", "r") as grosso:
        for line in grosso:
            article = json.loads(line)
            if 'url_tweet' in article:
                url = article['url_tweet']
                id = article['_id']
                if id not in id_news and url in url_buoni:
                    nuovo.write(line)
    grosso.close
    nuovo.close()

#find_otherNews()

# prende le notizie dal dataset tweetsCleaned
def getNews1():
    record = collection.find()
    dict = {}
    for doc in record:
        url = doc["url_tweet"]
        text = doc["url_text"].encode('ascii', 'ignore').decode('ascii')
        type = doc["type_page"]
        dict[url] = [text, type]
    print "creato il dict"

    keys = dict.keys()

    with open('/media/valentina/Data/tesi/testi1.json', 'w') as file:

        for k in keys:
            d = {"url": k, "text": dict[k][0], "type_page": dict[k][1]}
            json.dump(d, file)
            file.write("\n")
    file.close

# prende le notizie da nuove_news.json
def getNews2():
    collection2 = database["nuove"]
    record1 = collection.find()
    record2 = collection2.find()
    urls1 = set()
    for doc in record1:
        url = doc["url_tweet"]
        urls1.add(url)

    urls2 = set()
    for doc in record2:
        url = doc["url_tweet"]
        urls2.add(url)

    url_buoni = [x for x in urls2 if x not in urls1]

    source = open("/media/valentina/Data/tesi/dataset_mongo/dataset_twitter.json", "r")

    with open('/media/valentina/Data/tesi/testi2.json', 'w') as file:

        for line in source:
            article = json.loads(line)
            link = article["link"]
            for elem in url_buoni:
                if elem == link:
                    text = article["text"].encode('ascii', 'ignore').decode('ascii')
                    d = {"url": elem, "text": text, "type_page": article["type_page"]}
                    json.dump(d, file)
                    file.write("\n")
    file.close

    source.close()


getNews2()
