import pandas as pd
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
from unidecode import unidecode

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

myVar = "/home/luca/PycharmProjects/fake.csv"

mydata = pd.read_csv(myVar)
df = pd.DataFrame(mydata)

#cut real and fake dataframe to size 500
text = df["text"]

text_news = []
for i in range(len(text)):
    print(i)
    try:
        #text_news.append(text.iloc[i].encode('ascii', 'ignore').decode('ascii'))
        text2 = text.iloc[i]
        text_news.append(remove_non_ascii(str(text2)))
    except ValueError:
        # decoding failed
        continue
    except AttributeError:
        # decoding failed
        continue

# load the tokenizer and the model
myPickle = "/home/luca/PycharmProjects/FakeNewsDetection/Neural_networks/keras_tokenizer.pickle"
myModel = "/home/luca/PycharmProjects/FakeNewsDetection/Neural_networks/FakeNewsDetection_model.hdf5"
ValePickle = "/home/luca/PycharmProjects/Modello Rete Neurale nuovo/keras_tokenizer_new.pickle"
ValeModel = "/home/luca/PycharmProjects/Modello Rete Neurale nuovo/newmodel.hdf5"
with open(ValePickle, "rb") as f:
    tokenizer = pickle.load(f)

model = load_model(ValeModel)

sequences = tokenizer.texts_to_sequences(text_news)
data = pad_sequences(sequences, maxlen=1000)

# get predictions for each of your new texts
predictions = model.predict(data)
print(predictions)
cont_real = 0
cont_fake = 0
for prediction in predictions:
    if prediction <= 0.50 :
        cont_fake = cont_fake+1
        print("FAKE")
    else:
        cont_real = cont_real + 1
        print("REAL")

print("testi totali: ")
print(cont_fake + cont_real)
print ("totali predizioni errate (fake -> real ): ")
print(cont_real)
print ("totali predizioni giuste (fake -> fake): ")
print(cont_fake)

'''
#Save dataframes
real_text.to_pickle("real_news")
fake_text.to_pickle("fake_news")'''