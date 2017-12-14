import pandas as pd
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
from unidecode import unidecode
from Variables import *

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

mydata = pd.read_csv(fb_dataset)
df = pd.DataFrame(mydata)

#cut real and fake dataframe to size 500
text = df["text"]
labels = df["label"]
arraylabel= []
arraylabelpredicted = []
for elem in labels:
    arraylabel.append(elem)


text_news = []
for i in range(len(text)):
    print(i)
    try:
        #text_news.append(text.iloc[i].encode('ascii', 'ignore').decode('ascii'))
        text2 = text.iloc[i]
        text_news.append(remove_non_ascii(str(text2)))
    except ValueError:
        print("value error %d" %i)
    except AttributeError:
        print("attribute error %d" %i)


# load the tokenizer and the model
with open(tokenizer, "rb") as f:
    tokenizer = pickle.load(f)

model = load_model(neural_model)

sequences = tokenizer.texts_to_sequences(text_news)
data = pad_sequences(sequences, maxlen=700)

# get predictions for each of your new texts
predictions = model.predict(data)
print(predictions)
cont_real = 0
cont_fake = 0
for prediction in predictions:
    if prediction <= 0.50 :
        cont_fake = cont_fake+1
        arraylabelpredicted.append("fake")
        print("fake")
    else:
        cont_real = cont_real + 1
        arraylabelpredicted.append("real")
        print("real")

giuste = 0
errate= 0
for i in range(len(arraylabel)):
    if(arraylabel[i] == arraylabelpredicted[i]):
        giuste += 1
    else:
        errate += 1

print(arraylabel)
print(arraylabelpredicted)
print("..............................")

print("testi totali: ")
print(giuste + errate)
print ("totali predizioni errate: ")
print(errate)
print ("totali predizioni giuste: ")
print(giuste)
