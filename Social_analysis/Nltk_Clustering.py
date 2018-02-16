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
# normale solo real
with open("/media/valentina/Data/tesi/dataset_per_clustering/5News_user_real.json",'r') as dataset:
    for line in dataset:
        #if cont < 25:
            #print(cont)
            article = ast.literal_eval(line)
            text = article['text']
            news.append(text)
            #cont+=1

print len(news)



def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    text = text.translate(unicode(string.punctuation))
    tokens = word_tokenize(text)

    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    return tokens


def cluster_texts(texts, clusters=20):
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

clusters = cluster_texts(news, 20)
#pprint(dict(clusters))

cont2 = 0
i = 0
news_url= {}
#print(len(Min10NewsUser_real))
#my_json_dict = json.loads("/Scrivania/prova/provaaaaa.json")
#value1 = my_json_dict["id"+str(i)]['url']

# unico json solo real
myFile=open("/media/valentina/Data/tesi/dataset_per_clustering/5News_user_real_unico.json", 'r')
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
            #dict1[key]

#pprint(dict1)

news2 = {}
user_5news = news_associate(news2)
#print user_5news

news_lette = 0
#news_totali_utente = 0
user_cluster = {}
for key,value in user_5news.items():
    for keyDict, valueDict in dict1.items():
        for elem in value:
            #print "elem",elem
            for elemDict in valueDict:
                #print "elemendict:", elemDict
                if elem == elemDict:
                    news_lette+=1
        #news_totali_utente = float(news_lette)/float(len(valueDict))
        if news_lette > 0: #(float(len(valueDict)/2.0)):
            user_cluster.setdefault(key, [])
            user_cluster[key].append(news_lette)
        else:
            user_cluster.setdefault(key, [])
            user_cluster[key].append(0)
        #print user_cluster
        news_lette = 0

#print(user_cluster)
#print len(user_cluster)

utenti = open("/media/valentina/Data/tesi/utenti_ordinegiusto.txt", "r")
file = open("/media/valentina/Data/tesi/clustering_real.txt", "w")
for line in utenti:
    user = line.replace("\n", "")
    file.write(str(user) + ",")
    for elem in user_cluster[int(user)]:
        file.write(str(elem) + ",")
    file.write("\n")
file.close
utenti.close()





#value1 = myData["id"+str(i)]['url']

