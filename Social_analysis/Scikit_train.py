import json
from collections import Counter
from datetime import datetime
from Variables import *
from csv import reader
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier

# load pima indians dataset
with open(UserFeatures_matrix) as f:
    lines = (line for line in f if not line.startswith('#'))
    dataset = np.loadtxt(lines, delimiter=',', skiprows=1)
# split into input (X) and output (Y) variables

X = dataset[:,1:53]
sc = preprocessing.StandardScaler()
X_norm = sc.fit_transform(X)
Y = dataset[:,53]


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_norm, Y, test_size=0.20, random_state=42)

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
print("predizioni:")
print(preds[:10])
print("test:")
print(y_test[:10])

#Evaluate the model
from sklearn.metrics import accuracy_score
print("accuracy score:")
print(accuracy_score(y_test, preds))
print("\n")

#Average Precision
from sklearn.metrics import average_precision_score
print("average precision score")
print(average_precision_score(y_test, list(preds), average='macro', sample_weight=None))
print("\n")

#Log loss
from sklearn.metrics import zero_one_loss
print("loss:")
print(zero_one_loss(y_test, preds, normalize=True, sample_weight=None))
print("\n")


#Precision and Recall
from sklearn.metrics import classification_report
print(classification_report(y_test, preds))

'''import cPickle

with open('ScikitClassifier_UserFeatures.pkl', 'wb') as fid2:
    cPickle.dump(classifier, fid2)'''
