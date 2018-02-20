from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn.model_selection import StratifiedKFold
from Variables import *
import numpy as np
from sklearn import preprocessing

import numpy

seed = 7
np.random.seed(seed)


dataset = np.loadtxt(userMatrix, delimiter=",")
X = dataset[:,0:52]
Y = dataset[:,52]

sc = preprocessing.StandardScaler()
X_scale = sc.fit_transform(X)

kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
cvscores = []

for train, test in kfold.split(X_scale, Y):

    model = Sequential()
    model.add(Dense(20, input_dim=52, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(20, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_scale[train], Y[train], batch_size=10, verbose=0, epochs=10)
    scores = model.evaluate(X_scale[test],Y[test], verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    cvscores.append(scores[1] * 100)
# stampa la media e la deviazione standard
print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))