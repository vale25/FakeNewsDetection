import pandas as pd


mydata = pd.read_json("/home/luca/PycharmProjects/FakeNewsDetection/K-means_model/trainset_senza_duplicati.json", lines=True)
df = pd.DataFrame(mydata)

#select real and fake news from dataframe
real = df.loc[df['label'] == "REAL"]
fake = df.loc[df['label'] == "FAKE"]

#cut real and fake dataframe to size 500
real_text = real["text"][:100]
fake_text = fake["text"][:100]

#Save dataframes
real_text.to_pickle("real_news")
fake_text.to_pickle("fake_news")
