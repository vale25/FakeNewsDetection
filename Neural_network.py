from collections import Counter
from datetime import datetime
import json
from keras.layers import Embedding, LSTM, Dense, Conv1D, MaxPooling1D, Dropout, Activation
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

import numpy as np
import pickle

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

# comincio ad addestrare
tokenizer = Tokenizer(num_words=20000)
tokenizer.fit_on_texts(balanced_texts)
sequences = tokenizer.texts_to_sequences(balanced_texts)
data = pad_sequences(sequences, maxlen=700)

# uso pretrained embeddings con i dati di glove

embeddings_index = {}
glove_data = '/home/valentina/Documenti/tesi/testi/glove.6B.50d.txt'
f = open(glove_data)
for line in f:
    values = line.split()
    word = values[0]
    value = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = value
f.close()

print('Loaded %s word vectors.' % len(embeddings_index))



embedding_dimension = 50
word_index = tokenizer.word_index

embedding_matrix = np.zeros((len(word_index)+1, embedding_dimension))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector[:embedding_dimension]

print(embedding_matrix.shape)

embedding_layer = Embedding(embedding_matrix.shape[0],
                            embedding_matrix.shape[1],
                            weights=[embedding_matrix],
                            input_length=700)


model = Sequential()
#model.add(Embedding(20000, 128, input_length=700))

# utilizzo il layer embedded di glove
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