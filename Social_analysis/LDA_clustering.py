from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd
from Variables import *
import ast
from gensim import corpora, models, similarities
from itertools import chain

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


# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in news]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once] for text in texts]

# Create Dictionary.
id2word = corpora.Dictionary(texts)
# Creates the Bag of Word corpus.
mm = [id2word.doc2bow(text) for text in texts]

# Trains the LDA models.
lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=20, \
                               update_every=1, chunksize=10000, passes=1, minimum_probability=0,random_state=0)

# Prints the topics.
for top in lda.print_topics():
  print top
print

# Assigns the topics to the documents in corpus
lda_corpus = lda[mm]

# Find the threshold, let's set the threshold to be 1/#clusters,
# To prove that the threshold is sane, we average the sum of all probabilities:
scores = list(chain(*[[score for topic_id,score in topic] \
                      for topic in [doc for doc in lda_corpus]]))
threshold = sum(scores)/len(scores)
print threshold
print

cluster1 = [j for i,j in zip(lda_corpus,news) if i[0][1] > threshold]
cluster2 = [j for i,j in zip(lda_corpus,news) if i[1][1] > threshold]
cluster3 = [j for i,j in zip(lda_corpus,news) if i[2][1] > threshold]
cluster4 = [j for i,j in zip(lda_corpus,news) if i[3][1] > threshold]
cluster5 = [j for i,j in zip(lda_corpus,news) if i[4][1] > threshold]
cluster6 = [j for i,j in zip(lda_corpus,news) if i[5][1] > threshold]
cluster7 = [j for i,j in zip(lda_corpus,news) if i[6][1] > threshold]
cluster8 = [j for i,j in zip(lda_corpus,news) if i[7][1] > threshold]
cluster9 = [j for i,j in zip(lda_corpus,news) if i[8][1] > threshold]
cluster10 = [j for i,j in zip(lda_corpus,news) if i[9][1] > threshold]
cluster11= [j for i,j in zip(lda_corpus,news) if i[10][1] > threshold]
cluster12 = [j for i,j in zip(lda_corpus,news) if i[11][1] > threshold]
cluster13 = [j for i,j in zip(lda_corpus,news) if i[12][1] > threshold]
cluster14 = [j for i,j in zip(lda_corpus,news) if i[13][1] > threshold]
cluster15 = [j for i,j in zip(lda_corpus,news) if i[14][1] > threshold]
cluster16 = [j for i,j in zip(lda_corpus,news) if i[15][1] > threshold]
cluster17 = [j for i,j in zip(lda_corpus,news) if i[16][1] > threshold]
cluster18 = [j for i,j in zip(lda_corpus,news) if i[17][1] > threshold]
cluster19 = [j for i,j in zip(lda_corpus,news) if i[18][1] > threshold]
cluster20 = [j for i,j in zip(lda_corpus,news) if i[19][1] > threshold]

print cluster1
print cluster2
print cluster3
print cluster4
print cluster5
print cluster6
print cluster7
print cluster8
print cluster9
print cluster10
print cluster11
print cluster12
print cluster13
print cluster14
print cluster15
print cluster16
print cluster17
print cluster18
print cluster19
print cluster20


'''print len(cluster1)
print len(cluster2)
print len(cluster3)
print len(cluster4)
print len(cluster5)
print len(cluster6)
print len(cluster7)
print len(cluster8)
print len(cluster9)
print len(cluster10)
print len(cluster11)
print len(cluster12)
print len(cluster13)
print len(cluster14)
print len(cluster15)
print len(cluster16)
print len(cluster17)
print len(cluster18)
print len(cluster19)
print len(cluster20)'''
