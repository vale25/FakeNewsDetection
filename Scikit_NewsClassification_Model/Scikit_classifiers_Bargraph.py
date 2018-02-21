import json
from collections import Counter
from datetime import datetime
from Variables import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier

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

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(vectors, labels, test_size=0.33, random_state=42)

from sklearn.svm import LinearSVC

# initialise the SVM classifier
classifier = LinearSVC()


# train the classifier
t1 = datetime.now()
classifier.fit(X_train, y_train)
print("Tempo di train:")
print(datetime.now() - t1)

#Make prediction
preds = classifier.predict(X_test)
print(list(preds[:10]))
print(y_test[:10])

#Evaluate the model
from sklearn.metrics import accuracy_score
svc_score = accuracy_score(y_test, preds)


classifier = KNeighborsClassifier()

# train the classifier
t1 = datetime.now()
classifier.fit(X_train, y_train)
print("Tempo di train:")
print(datetime.now() - t1)

#Make prediction
preds = classifier.predict(X_test)
print(list(preds[:10]))
print(y_test[:10])

#Evaluate the model
knn_score = accuracy_score(y_test, preds)



classifier = SGDClassifier()

# train the classifier
t1 = datetime.now()
classifier.fit(X_train, y_train)
print("Tempo di train:")
print(datetime.now() - t1)

#Make prediction
preds = classifier.predict(X_test)
print("------------------------- %d" %len(preds))
print(list(preds[:10]))
print(y_test[:10])

#Evaluate the model
sgd_score = accuracy_score(y_test, preds)


#MATH RANDOM
import random

bin = []
preds = []
for i in range(0, 2000):
    a = random.randint(0, 1)
    bin.append(a)

for elem in bin:
    if elem == 0:
        preds.append("FAKE")
    else:
        preds.append("REAL")

#Evaluate the model
math_score = accuracy_score(y_test, preds)




import matplotlib.pyplot as plt
import pandas as pd

data = {'Linear SVC': {"":svc_score}, 'K-NN':{"":knn_score} , 'SGD':{"":sgd_score}, 'math.random':{"":math_score} }

df = pd.DataFrame(data)

df.plot(kind='bar')


plt.show()