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
    reviews = f.read().strip().split("\n")

reviews = [json.loads(review) for review in reviews]
print(datetime.now() - t1)

# Get a balanced sample of real and fake reviews
texts = [review['title'] for review in reviews]

# Convert our 5 classes into 2 (negative or positive)
binfake = [0 if review['label'] == "FAKE" else 1 for review in reviews]
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

model = Sequential()
model.add(Embedding(20000, 128, input_length=700))
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