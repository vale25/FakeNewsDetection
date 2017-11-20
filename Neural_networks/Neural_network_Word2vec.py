from collections import Counter
from datetime import datetime
import json
from keras.layers import Embedding, LSTM, Dense, Conv1D, MaxPooling1D, Dropout
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from gensim.models import KeyedVectors

import numpy as np
import pickle

t1 = datetime.now()
with open("/home/valentina/Documenti/tesi/trainset_senza_duplicati.json") as f:
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

# comincio ad addestrare
tokenizer = Tokenizer(num_words=20000)
tokenizer.fit_on_texts(balanced_texts)
sequences = tokenizer.texts_to_sequences(balanced_texts)
data = pad_sequences(sequences, maxlen=700)

# fino a limit=400k va abbastanza velocemente
w2v_model = KeyedVectors.load_word2vec_format('/media/valentina/Data/pretrained_data/GoogleNews-vectors-negative300.bin',
                                              limit=500000, binary=True)
# creo la matrice
embedding_matrix = w2v_model.syn0

print(embedding_matrix.shape)

embedding_layer = Embedding(embedding_matrix.shape[0], embedding_matrix.shape[1],
                            weights=[embedding_matrix], input_length=700)

model = Sequential()
# utilizzo il layer creato con il file di word2vec
model.add(embedding_layer)

model.add(Dropout(0.2))
model.add(Conv1D(64, 5, activation='relu'))
model.add(MaxPooling1D(pool_size=4))
model.add(LSTM(128))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(data, np.array(balanced_labels), batch_size=64, validation_split=0.25, epochs=3)

# save the tokenizer and model
#with open("keras_tokenizer.pickle", "wb") as f:
#    pickle.dump(tokenizer, f)
#model.save("FakeNewsDetection_model_giusto.hdf5")