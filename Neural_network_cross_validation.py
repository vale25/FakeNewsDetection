from collections import Counter
from datetime import datetime
import json
from keras.layers import Embedding, LSTM, Dense, Conv1D, MaxPooling1D, Dropout, Activation
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import StratifiedKFold

import numpy
import pickle

seed = 7
numpy.random.seed(seed)

t1 = datetime.now()
with open("trainset_senza_duplicati.json") as f:
    articles = f.read().strip().split("\n")

articles = [json.loads(article) for article in articles]
print(datetime.now() - t1)

texts = [article['text'] for article in articles]

binfake = [0 if article['label'] == "FAKE" else 1 for article in articles]
balanced_texts = []
balanced_labels = []
limit = 100000  # Change this to grow/shrink the dataset
neg_pos_counts = [0, 0]
for i in range(len(texts)):
    polarity = binfake[i]
    if neg_pos_counts[polarity] < limit:
        balanced_texts.append(texts[i])
        balanced_labels.append(binfake[i])
        neg_pos_counts[polarity] += 1
print(balanced_labels)

print(Counter(balanced_labels))

tokenizer = Tokenizer(num_words=20000)
tokenizer.fit_on_texts(balanced_texts)
sequences = tokenizer.texts_to_sequences(balanced_texts)
data = pad_sequences(sequences, maxlen=700)

kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
cvscores = []

for train, test in kfold.split(data, numpy.array(balanced_labels)):

    model = Sequential()
    model.add(Embedding(20000, 128, input_length=700))
    model.add(Dropout(0.2))
    model.add(Conv1D(64, 5, activation='relu'))
    model.add(MaxPooling1D(pool_size=4))
    model.add(LSTM(128))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(data[train], numpy.array(balanced_labels)[train], batch_size=64, verbose=0, epochs=3)
    scores = model.evaluate(data[test],numpy.array(balanced_labels)[test], verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    cvscores.append(scores[1] * 100)
# stampa la media e la deviazione standard
print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))

# save the tokenizer and model
with open("keras_tokenizer.pickle", "wb") as f:
   pickle.dump(tokenizer, f)
model.save("CrossValidation_model_giusto.hdf5")