import string
import collections
from GetFeatures import news_associate
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint
from Variables import *
import ast
import json

cont = 0
news = []
with open(Min10NewsUser_real_noSons,'r') as dataset:
    for line in dataset:
        if cont < 25:
            print(cont)
            article = ast.literal_eval(line)
            text = article['text']
            news.append(text)
            cont+=1



def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    text = text.translate(unicode(string.punctuation))
    tokens = word_tokenize(text)

    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    return tokens


def cluster_texts(texts, clusters=10):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 max_df=0.5,
                                 min_df=0.1,
                                 lowercase=True)

    tfidf_model = vectorizer.fit_transform(texts)
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_model)

    clustering = collections.defaultdict(list)

    #idx rappresenta l'indice della notizia e la label l'etichetta numerica del cluster
    #Questo ciclo assegna ad ogni cluster la notizia che vi rientra al suo interno
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)

    return clustering

clusters = cluster_texts(news, 10)
pprint(dict(clusters))

cont2 = 0
i = 0
news_url= {}
#print(len(Min10NewsUser_real))
#my_json_dict = json.loads("/Scrivania/prova/provaaaaa.json")
#value1 = my_json_dict["id"+str(i)]['url']


myFile=open(Min10NewsUser_real, 'r')
myObject=myFile.read()
u = myObject.decode('utf-8-sig')
myObject = u.encode('utf-8')
myFile.encoding
myFile.close()
myData=json.loads(myObject,'utf-8')

dict1 = {}
dict_clusters = dict(clusters)
for key,value in dict_clusters.items():
        for elem in value:
           # print elem
            dict1.setdefault(key, [])
            dict1[key].append(myData["id"+str(elem)]['url'])

print dict1

'''news = {}
news.setdefault("123", []).append("http://giantswire.usatoday.com/?p=602654")
news.setdefault("123", []).append("http://www.chicagotribune.com/news/local/breaking/ct-met-chicago-violence-shootings-20180115-story.html?utm_source=dlvr.it&utm_medium=twitter")
news.setdefault("233", []).append("http://www.chicagotribune.com/news/local/breaking/ct-met-chicago-violence-shootings-20180115-story.html")
news.setdefault("233", []).append("https://www.chron.com/news/houston-texas/article/texas-flu-vaccine-anti-vaxxer-get-flu-shot-trump-12556371.php?utm_source=dlvr.it&utm_medium=twitter")
news.setdefault("234", []).append("http://www.chicagotribune.com/news/local/breaking/ct-met-fatal-logan-square-fire-20180110-story.html")
news.setdefault("134", []).append("https://nypost.com/2018/01/29/76-immigrants-found-stuffed-inside-tractor-trailer-in-texas-officials/")
user_5news = news
print user_5news'''


user_5news = news_associate(news)

news_lette = 0
news_totali_utente = 0
user_cluster = {}
for key,value in user_5news.items():
    for keyDict, valueDict in dict1.items():
        for elem in value:
            #print "elem",elem
            for elemDict in valueDict:
                #print "elemendict:", elemDict
                if elem == elemDict:
                    news_lette+=1
        news_totali_utente = float(news_lette)/float(len(valueDict))
        if news_totali_utente >= (float(len(valueDict)/2.0)):
            user_cluster.setdefault(key, [])
            user_cluster[key].append(keyDict)
        news_lette = 0

print(user_cluster)






#value1 = myData["id"+str(i)]['url']

