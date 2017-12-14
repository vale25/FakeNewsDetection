import cPickle as pickle
import pandas as pd
from Variables import *

with open('Kmeans_vectorizer.pkl', 'rb') as f:
    vect = pickle.load(f)

with open('Kmeans_cluster.pkl', 'rb') as f:
    km = pickle.load(f)

print("Prediction")

mydata = pd.read_json(trainset_senza_duplicati, lines=True)
df = pd.DataFrame(mydata)

Y = vect.transform(["October 31, 2016 at 4:52 am \nPretty factual except for women in the selective service. American military is still voluntary only and hasn't been a draft since Vietnam war. The comment was made by a 4 star general of the army about drafting women and he said it to shut up liberal yahoos."]) #fake
prediction = km.predict(Y)
print(prediction)

Y = vect.transform(["NEW YORK, N.Y. - If Hillary Clinton is winning the Democratic presidential race, why has it felt like she's losing? Yes, Mrs. Clinton scored an important victory in New York Tuesday, winning her adopted home state in the primary. But should the outcome ever have been in doubt? As a former senator from New York she"]) #real
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