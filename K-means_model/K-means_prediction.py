import cPickle as pickle
import pandas as pd

with open('Kmeans_vectorizer.pkl', 'rb') as f:
    vect = pickle.load(f)

with open('Kmeans_cluster.pkl', 'rb') as f:
    km = pickle.load(f)

print("Prediction")

mydata = pd.read_json("trainset_senza_duplicati.json", lines=True)
df = pd.DataFrame(mydata)

Y = vect.transform(["chrome browser to open."])
prediction = km.predict(Y)
print(prediction)

Y = vect.transform(["My cat is hungry."])
prediction = km.predict(Y)
print(prediction)


from sklearn.model_selection import train_test_split
# split features and labels (e.g. test = 20%,training = 80% )
# try both bag of words and tfidf features
x_train, x_test, y_train, y_test = train_test_split(vect.transform(df.text.tolist()), mydata['label'].values, test_size=0.2)
print("Training the random forest...")
from sklearn.ensemble import RandomForestClassifier
# Initialize a Random Forest classifier with 100 trees
forest = RandomForestClassifier(n_estimators = 100)
# Fit the forest to the training set, using the tfidf as
# features and the sentiment labels as the response variable
# This may take a few minutes to run
forest_model = forest.fit(x_train, y_train)


# Use the random forest model to make sentiment label predictions
y_pred = forest_model.predict( x_test )
# evaluate accuracy using hamming loss metric
from sklearn.metrics import hamming_loss
print(1 - hamming_loss(y_pred, y_test))