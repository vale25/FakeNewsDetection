from sklearn.model_selection import cross_val_score
from Variables import *
import numpy as np
from sklearn import preprocessing
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC




# load dataset
with open(UserFeatures_matrix) as f:
    lines = (line for line in f if not line.startswith('#'))
    dataset = np.loadtxt(lines, delimiter=',', skiprows=1)

#Split the dataset
X = dataset[:,13:53]
sc = preprocessing.StandardScaler()
#X_norm = preprocessing.normalize(X)
X_norm = sc.fit_transform(X)
Y = dataset[:,53]


X_train, X_test, y_train, y_test = train_test_split(X_norm, Y, test_size=0.2, random_state=0)


# initialise the SVM classifier
#classifier = LinearSVC()
#classifier = KNeighborsClassifier()
classifier = SGDClassifier()
scores = cross_val_score(classifier, X_train, y_train, cv=10)
cont = 0
for elem in scores:
    print("Accuracy split %d : %f" %(cont, elem))
    cont+=1

print("\nMean accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

