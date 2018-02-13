import re
from pymongo import MongoClient
from collections import Counter
from User_News_Twitter import activeUsers
from Variables import *
import ast
import json

client = MongoClient('localhost:27017')

database = client['twitter']
collection = database['tweets']

record = collection.find()

# prendo gli id degli utenti che hanno letto almeno 10 news
users_id = activeUsers().keys()
#print users_id

news = collection.aggregate([{"$group": { "_id": "$Tweet.user.id", "id_news": { "$addToSet": "$_id"} } }])


record = collection.find({"Tweet.user.id": {"$in":users_id} })
print record.count()

url_news = []
cont = 0
vuote = 0
for doc in record:
    tweet = doc["url_tweet"]
    print(tweet)
    if tweet == "":
        vuote+=1
        print("tweet vuoto", cont)
    else:
        url_news.append(tweet)

url_news_noDuplicati = list(set(url_news))
print("vuote:", vuote)
print("lunghezza url news", len(url_news))
print("lunghezza url news senza duplicati", len(url_news_noDuplicati))


outfile = open('/media/luca/Windows8_OS/Json_dataset_FakeReal_Twitter/dataset_twitter_finale/10News_user.json', 'w')

contatore = 0
with open(ExtractedNews_twitter,'r') as dataset:
    for line in dataset:
        print contatore
        article = ast.literal_eval(line)
        url = article['url']
        for elem in url_news_noDuplicati:
            if url == elem:
                print("uguali")
                outfile.write(line)

        contatore+=1

    dataset.close
    outfile.close



