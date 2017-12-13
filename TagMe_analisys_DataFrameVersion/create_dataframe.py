import pandas as pd

Lucavar_trainset = "/home/luca/PycharmProjects/FakeNewsDetection/K-means_model/trainset_senza_duplicati.json"

mydata = pd.read_json(Lucavar_trainset, lines=True)
df = pd.DataFrame(mydata)

#select real and fake news from dataframe
real = df.loc[df['label'] == "REAL"]
fake = df.loc[df['label'] == "FAKE"]

#cut real and fake dataframe to size 500
real_text = real["text"]
fake_text = fake["text"]

#Save dataframes
real_text.to_pickle("real_news")
fake_text.to_pickle("fake_news")
