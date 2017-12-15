from datetime import datetime
import pandas as pd
import pickle
from unidecode import unidecode
from Variables import *

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

mydata = pd.read_csv(fb_dataset)
df = pd.DataFrame(mydata)

#Select text from dataset
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
        # decoding failed
        continue
    except AttributeError:
        # decoding failed
        continue


# load model
with open(Scikit_vectorizer, 'rb') as f:
    clf1 = pickle.load(f)

with open(Scikit_classifier, 'rb') as f:
    clf2 = pickle.load(f)
t1 = datetime.now()


vecs = clf1.transform(text_news)
errate = 0
giuste = 0
# predict a real or fake label for each input
predictions = clf2.predict(vecs)

#Create list of prediction for analisys
for elem in predictions:
    if elem == "FAKE":
        #arraylabelpredicted.append(elem.lower())
        arraylabelpredicted.append("fake")
    else:
        arraylabelpredicted.append("real")

for i in range(len(arraylabel)):
    if arraylabel[i] == arraylabelpredicted[i]:
        giuste +=1
    else:
        errate +=1

tot = errate + giuste
print(arraylabel)
print(arraylabelpredicted)
print("------------------------------------------------------")
print("totale news %d" %tot)
print("Predizioni giuste %d" %giuste)
print("Predizioni errate %d" %errate)