from datetime import datetime
from Variables import *
import numpy as np
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier

# load dataset
with open(UserFeatures_matrix) as f:
    lines = (line for line in f if not line.startswith('#'))
    dataset = np.loadtxt(lines, delimiter=',', skiprows=1)
# split into input (X) and output (Y) variables

X = dataset[:,1:53]
sc = preprocessing.StandardScaler()
#X_norm = preprocessing.normalize(X)
X_norm = sc.fit_transform(X)
Y = dataset[:,53]


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_norm, Y, test_size=0.20, random_state=0)

from sklearn.svm import LinearSVC

# initialise the SVM classifier
classifier = LinearSVC()
classifier.fit(X_train, y_train)


#Make prediction
preds = classifier.predict(X_test)
print("predizioni:")
print(preds[:10])
print("test:")
print(y_test[:10])

#Evaluate the model
from sklearn.metrics import accuracy_score
svc_score = accuracy_score(y_test, preds)
print("accuracy score:")
print(accuracy_score(y_test, preds))
print("\n")


classifier = KNeighborsClassifier()
classifier.fit(X_train, y_train)


#Make prediction
preds = classifier.predict(X_test)
print("predizioni:")
print(preds[:10])
print("test:")
print(y_test[:10])

#Evaluate the model
from sklearn.metrics import accuracy_score
knn_score = accuracy_score(y_test, preds)
print("accuracy score:")
print(accuracy_score(y_test, preds))
print("\n")



classifier = SGDClassifier()
classifier.fit(X_train, y_train)


#Make prediction
preds = classifier.predict(X_test)
print("predizioni:")
print(preds[:10])
print("test:")
print(y_test[:10])

#Evaluate the model
from sklearn.metrics import accuracy_score
print("accuracy score:")
sgd_score = accuracy_score(y_test, preds)
print(accuracy_score(y_test, preds))
print("\n")




import matplotlib.pyplot as plt
import pandas as pd

data = {'Linear SVC': {"":svc_score}, 'K-NN':{"":knn_score} , 'SGD':{"":sgd_score} }

df = pd.DataFrame(data)

df.plot(kind='bar')


plt.show()