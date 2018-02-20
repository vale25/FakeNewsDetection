from sklearn.model_selection import cross_val_score
from Variables import *
import numpy as np
from sklearn import preprocessing
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
import json
from collections import Counter
from datetime import datetime

# read the data from disk and split into lines
# we use .strip() to remove the final (empty) line
with open(trainset_senza_duplicati) as f:
    news = f.read().strip().split("\n")

# each line of the file is a separate JSON object
news = [json.loads(line) for line in news]

# we're interested in the text of each review
# and the stars rating, so we load these into
# separate lists
texts = [review['text'] for review in news]
labels = [review['label'] for review in news]

print(Counter(labels))

from sklearn.feature_extraction.text import TfidfVectorizer

# This vectorizer breaks text into single words and bi-grams
# and then calculates the TF-IDF representation
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
t1 = datetime.now()

# the 'fit' builds up the vocabulary from all the news
# while the 'transform' step turns each individual text into
# a matrix of numbers.
vectors = vectorizer.fit_transform(texts)
print("Tempo di vettorizzazione:")
print(datetime.now() - t1)

#Split in train and test
X_train, X_test, y_train, y_test = train_test_split(vectors, labels, test_size=0.2, random_state=0)


# initialise the SVM classifier
#classifier = LinearSVC()
#classifier = KNeighborsClassifier()
classifier = SGDClassifier()
scores = cross_val_score(classifier, X_train, y_train, cv=10)
cont=0
for elem in scores:
    print("Accuracy split %d : %f" %(cont, elem))
    cont+=1

print("\nMean accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))