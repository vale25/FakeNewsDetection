
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn.model_selection import train_test_split

from Variables import userMatrix, userMatrix_features, userMatrix_clusters
from sklearn import preprocessing

import numpy as np

seed = 7
np.random.seed(seed)

dataset = np.loadtxt(userMatrix, delimiter=",")
X = dataset[:,0:52]
Y = dataset[:,52]

sc = preprocessing.StandardScaler()
X = sc.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=seed)

def standardModel():
    model = Sequential()
    model.add(Dense(20, input_dim=52, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(20, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


model = standardModel()

#model.fit(X_norm, Y, batch_size=10, validation_split=0.2, epochs=100)
model.fit(X_train, y_train, batch_size=10, validation_split=0.2, epochs=10)
score = model.evaluate(X_test, y_test, verbose=0)
print("test loss: ", score[0])
print("test accuracy: ", score[1])