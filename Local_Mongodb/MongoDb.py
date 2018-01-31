import re
from boilerpipe.extract import Extractor
from pymongo import MongoClient
from urllib2 import URLError
from urllib2 import HTTPError
from socket import timeout
from httplib import BadStatusLine
import logging

def extraction(link):
    extractor = Extractor(extractor='ArticleExtractor', url=link)
    extracted_text = extractor.getText()
    return extracted_text

client = MongoClient('localhost:27017')

database = client['twitter']
collection = database['tweets']
record = collection.find().count()

#Query per ottenere i primi 100 elementi che non hanno campo url_text e che hanno campo urlEntities non vuoto ed in urlEntities non hanno https://twitter.co
NoLinkTwitter = collection.find({"url_text":{'$exists':False},"Tweet.urlEntities":{'$exists':True},"Tweet.urlEntities":{'$not': {'$size' : 0}},"Tweet.urlEntities.expandedURL":{'$not' : re.compile("https://twitter.com")}})
NoLinkTwitterCount = collection.find({"url_text":{'$exists':False},"Tweet.urlEntities":{'$exists':True},"Tweet.urlEntities":{'$not': {'$size' : 0}},"Tweet.urlEntities.expandedURL":{'$not' : re.compile("https://twitter.com")}}).count()
print(NoLinkTwitterCount)

#Query per prendere i documenti con url_text buono
url_text_buono = collection.find({'$nor': [{ "url_text:": {"$regex" : "utilizzando i servizi","$options" : "i"}}, {"url_text": {"$regex" : "su Twitter"}},{"url_text": {"$regex" : "by using Twitter", "$options" : "i"}}], "url_text": {"$exists": True}, "$where": "this.url_text.length > 1100"})

#Query per trovare documenti con due url di cui il primo e' buono ed il secondo un rimando al post di twitter
#dueUrlTwitter = collection.find({"Tweet.urlEntities" : {"$exists" : True, "$size" : 2}, "Tweet.urlEntities.expandedURL": {"$regex": "https://twitter.com", "$options": "s"}, "url_text": "", "Tweet.retweetedStatus": {"$exists": False}}).count()
dueUrlTwitterConRetweet = collection.find({"Tweet.urlEntities" : {"$exists" : True, "$size" : 2}, "Tweet.urlEntities.expandedURL": {"$regex": "https://twitter.com", "$options": "s"}, "url_text": ""})

#Query per trovare i documenti con url_text vuoto ma con link buono per Boilerpipe in urlEntities
link_con_url_text_vuoto = collection.find({"Tweet.urlEntities": {"$exists": True, "$size": 1}, "Tweet.urlEntities.expandedURL": {"$not": re.compile("https://twitter.com")}, "url_text": ""})

#Query per trovare documenti con due url di cui il secondo e' buono ed il primo un rimando al post di twitter
dueUrlTwitterSecondoBuono = collection.find({"Tweet.urlEntities": {"$exists": True, "$size": 2}, "url_text": "", "Tweet.urlEntities.expandedURL": {"$not": re.compile("https://twitter.com")}})

#Query per torvare documenti con url_text vuoto, urlEntities vuoto ma urlEntities sta nel campo retweetedStatus
urlEntitiesInRetweet = collection.find({"Tweet.urlEntities": {"$size": 0}, "url_text": "", "Tweet.retweetedStatus": {"$exists":True}, "Tweet.retweetedStatus.urlEntities": {"$exists": True, "$size": 1}, "Tweet.retweetedStatus.urlEntities.expandedURL": {"$not": re.compile("https://twitter.com")}})


'''client = MongoClient()
db = client.News

#49
#Crea la set list urlTwitter per eliminare i doppioni ed appendi expandedUrl e type page dei documenti di NoLinkTwitter
urlTwitter = []
for doc in NoLinkTwitter:
    tweet = doc['Tweet']
    type_page = doc["type_page"]
    urlEntities = tweet["urlEntities"]
    expandedURL = urlEntities[0]['expandedURL']
    urlTwitter.append((expandedURL,type_page))

#tot doc = 12001
#Appendi alla lista urlTwitter il campo expandedUrl e type page di ogni doc di urlEntitiesInRetweet
for doc in urlEntitiesInRetweet:
    tweet = doc['Tweet']
    type_page = doc["type_page"]
    #Entra nel campo retweetedStatus
    retweetedStatus = tweet["retweetedStatus"]
    urlEntities = retweetedStatus['urlEntities']
    expandedURL = urlEntities[0]['expandedURL']
    urlTwitter.append((expandedURL,type_page))


#tot doc = 74615
#Appena alla lista di urlTwitter l'expandedUrl ed il tipo di pagina dei doc di link_con_url_text_vuoto per rimuovere di doppioni dalla query link_con_url_text_vuoto
for doc in link_con_url_text_vuoto:
    tweet = doc['Tweet']
    type_page = doc["type_page"]
    urlEntities = tweet["urlEntities"]
    expandedURL = urlEntities[0]['expandedURL']
    urlTwitter.append((expandedURL,type_page))


#tot doc = 1770
#Appendi alla lista urlTwitter per rimuovere di doppioni dalla query dueUrlTwitterConRetweet
for doc in dueUrlTwitterConRetweet:
    tweet = doc['Tweet']
    type_page = doc["type_page"]
    urlEntities = tweet["urlEntities"]
    expandedURL = urlEntities[0]['expandedURL']
    urlTwitter.append((expandedURL,type_page))


#tot doc = 7891
#Appendi alla lista urlTwitter per rimuovere di doppioni dalla query dueUrlTwitterSecondoBuono
for doc in dueUrlTwitterSecondoBuono:
    tweet = doc['Tweet']
    type_page = doc["type_page"]
    urlEntities = tweet["urlEntities"]
    expandedURL = urlEntities[1]['expandedURL']
    urlTwitter.append((expandedURL,type_page))

urlTwitterSenzaDuplicati = list(set(urlTwitter))

#Itera sulla lista senza duplicati per applicare Boilerpipe e inserire le notizie nei dataset Real o Fake in base al tipo di pagina
contatore = 0
print(len(urlTwitterSenzaDuplicati))
print("--------------------------------------------------------------")
for elem in urlTwitterSenzaDuplicati:
    try :
        print(elem[0])
        #Usa BoilerPipe sull'URL ottenuto dalla query per ottenere il testo di ciascun tweet
        text = extraction(elem[0])
        #Se la notizia e' Mainstream inseriscila nel dataset Real
        if elem[1] == "Mainstream":
            result = db.RealNews.insert_one(
                {
                    "type_page": type_page,
                    "link": elem[0],
                    "text": text
                }
            )

        # Se la notizia e' misinformation inseriscila nel dataset Fake
        if elem[1] == "misinformation":
            result = db.FakeNews.insert_one(
                {
                    "type_page": type_page,
                    "link": elem[0],
                    "text": text
                }
            )
    except (HTTPError, URLError) as error:
        logging.error('Data is not retrieved because %s\nURL: %s', error, elem[0])
    except timeout:
        logging.error('socket timed out - URL %s', elem[0])
    except BadStatusLine:
        print ("could not fetch %s" % elem[0])
    print(contatore)
    contatore+=1'''

client = MongoClient()
db = client.NewsTogliDuplicati



#tot doc = 85656
#Itera sugli elementi di url_text_buono:
for doc in url_text_buono:
    tweet = doc['Tweet']
    url_text = doc["url_text"]
    type_page = doc["type_page"]
    urlEntities = tweet["urlEntities"]
    expandedURL = urlEntities[0]['expandedURL']
    print(type_page)
    if type_page == "Mainstream":
        result = db.RealNews.insert_one(
            {
                "type_page": type_page,
                "link": expandedURL,
                "text": url_text
            }
        )
    if type_page == "misinformation":
        result = db.FakeNews.insert_one(
            {
                "type_page": type_page,
                "link": expandedURL,
                "text": url_text
            }
        )


#TOTALE DOCUMENTI CON DUPLICATI 181891 SU 321314 INIZIALI DEL DATASET

