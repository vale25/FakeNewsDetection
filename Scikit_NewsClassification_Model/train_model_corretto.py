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
#classifier = LinearSVC()
#classifier = KNeighborsClassifier()
classifier = SGDClassifier()

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
print("accuracy score:\n")
print(accuracy_score(y_test, preds))
print("\n")

y_test_bin = []
preds_bin= []
for elem in y_test:
    if elem == "FAKE":
        y_test_bin.append(0)
    else:
        y_test_bin.append(1)

for elem in preds:
    if elem == "FAKE":
        preds_bin.append(0)
    else:
        preds_bin.append(1)

#Average Precision
from sklearn.metrics import average_precision_score
print("average precision score:\n")
print(average_precision_score(y_test_bin, preds_bin, average='macro', sample_weight=None))
print("\n")

#Log loss
from sklearn.metrics import zero_one_loss
print("loss:\n")
print(zero_one_loss(y_test, preds, normalize=True, sample_weight=None))
print("\n")


#Precision and Recall
from sklearn.metrics import classification_report
print(classification_report(y_test, preds))

'''import cPickle
# save the classifier
with open('ScikitVectorizer.pkl', 'wb') as fid:
    cPickle.dump(vectorizer, fid)

with open('ScikitClassifier.pkl', 'wb') as fid2:
    cPickle.dump(classifier, fid2)'''
