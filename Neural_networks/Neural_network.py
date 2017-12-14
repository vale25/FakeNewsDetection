from collections import Counter
from datetime import datetime
import json
from keras.layers import Embedding, LSTM, Dense, Conv1D, MaxPooling1D, Dropout, Activation
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from Variables import *

import numpy as np
import pickle

t1 = datetime.now()
with open(trainset_senza_duplicati) as f:
    articles = f.read().strip().split("\n")

articles = [json.loads(article) for article in articles]
print(datetime.now() - t1)

texts = [article['text'] for article in articles]

binfake = [0 if article['label'] == "FAKE" else 1 for article in articles]
balanced_texts = []
balanced_labels = []
# usa questo parametro se il dataset e' molto grande per decidere quante news fake e real considerare
limit = 10000
neg_pos_counts = [0, 0]
for i in range(len(texts)):
    polarity = binfake[i]
    if neg_pos_counts[polarity] < limit:
        balanced_texts.append(texts[i])
        balanced_labels.append(binfake[i])
        neg_pos_counts[polarity] += 1
print(balanced_labels)

print(Counter(balanced_labels))

# comincio ad addestrare

# num_words: le prime n parole piu' frequenti vengono incluse nel vocabolario
tokenizer = Tokenizer(num_words=30000)

tokenizer.fit_on_texts(balanced_texts)
sequences = tokenizer.texts_to_sequences(balanced_texts)
print (len(tokenizer.word_index))
data = pad_sequences(sequences, maxlen=1000)

model = Sequential()

model.add(Embedding(30000, 128, input_length=1000))
model.add(Dropout(0.2))
model.add(Conv1D(64, 5, activation='relu'))
model.add(MaxPooling1D(pool_size=4))
model.add(LSTM(128))
model.add(Dense(1, activation='sigmoid'))

# con queste due righe realizzo una rete neurale ricorrente semplice, piu' lenta
#model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
#model.add(Dense(1, activation='sigmoid'))
#

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(data, np.array(balanced_labels), batch_size=64, validation_split=0.25, epochs=2)

# save the tokenizer and model
#with open("keras_tokenizer.pickle", "wb") as f:
#    pickle.dump(tokenizer, f)
#model.save("FakeNewsDetection_model_giusto.hdf5")