from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
from boilerpipe.extract import Extractor
import pymongo
from Variables import *

# load the tokenizer and the model
with open(tokenizer, "rb") as f:
    tokenizer = pickle.load(f)

model = load_model(neural_model)
news_link = []
user = "luca04"
password = "pinguepinga1"

client = pymongo.MongoClient("mongodb://%s:%s@ds111876.mlab.com:11876/politicsnewsdb" %(user, password))

#Prendi i link da ogni documento di mongodb
db = client.politicsnewsdb
result = db.politicsnewsdb.find()
for document in result:
    text = str(document["link"])
    news_link.append(text)
    #print(document["link"])

print(news_link)
news_text = []

def extraction(link):
    extractor = Extractor(extractor='ArticleExtractor', url=link)
    extracted_text = extractor.getText()
    if extracted_text  != "" or extracted_text != None :
        news_text.append(extracted_text)

for i in range(len(news_link)):
    extraction(news_link[i])
    '''extractor = Extractor( extractor='ArticleExtractor', url= news_link[i] )

    extracted_text = extractor.getText()
    if extracted_text  != "" or extracted_text != None :
        news_text.append(extracted_text)'''

print(news_text)
#print(text)
#print("")

#extracted_html = extractor.getHTML()
#print (extracted_html)

sequences = tokenizer.texts_to_sequences(news_text)
data = pad_sequences(sequences, maxlen=700)

# get predictions for each of your new texts
predictions = model.predict(data)
print(predictions)
for prediction in predictions:
    if prediction <= 0.50 :
        print("FAKE")
    else:
        print("REAL")




