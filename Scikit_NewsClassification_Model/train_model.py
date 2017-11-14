import pandas as pd

#mydata = pd.read_csv("fake_or_real_news.csv", header=0)
#original_headers = list(mydata.columns.values[0])
#numpy_array = mydata.as_matrix()
mydata = pd.read_json("trainset_senza_duplicati.json", lines=True)
df = mydata.loc[:, 'text'].tolist()

array_label = []
for i in range(len(mydata)):
    array_label.append(mydata.label[i])
    i = i+1

array_int = []
for j in range(len(array_label)):
    if array_label[j] == ("FAKE"):
        array_int.append(0)
    else:
        array_int.append(1)
    j = j+1

mydata['target'] = array_int
#mydata['target_names'] = array_label
#print(mydata.target.values)
#datalist2 = list(set(mydata.label.tolist()))
datalistLabel = mydata.label.tolist()
#print(datalistLabel)
#print(mydata.target_names.values)

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(df)
X_train_counts.shape
print(count_vect.vocabulary_.get(u'algorithm'))

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print(X_train_tfidf.shape)

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, mydata.target.values)

docs_new = ['Donald Trump is an alien', 'Killing Obama administration rules, dismantling Obamacare and pushing through tax reform are on the early to-do list.','U.S. Secretary of State John F. Kerry said Monday that he will stop in Paris later this week, amid criticism that no top American officials attended Sunday\'s unity march against terrorism.\n\nKerry said he expects to arrive in Paris Thursday evening, as he heads home after a week abroad. He said he will fly to France at the conclusion of a series of meetings scheduled for Thursday in Sofia, Bulgaria. He plans to meet the next day with Foreign Minister Laurent Fabius and President Francois Hollande, then return to Washington.\n\nThe visit by Kerry, who has family and childhood ties to the country and speaks fluent French, could address some of the criticism that the United States snubbed France in its darkest hour in many years.\n\nThe French press on Monday was filled with questions about why neither President Obama nor Kerry attended Sunday\'s march, as about 40 leaders of other nations did. Obama was said to have stayed away because his own security needs can be taxing on a country, and Kerry had prior commitments.\n\nAmong roughly 40 leaders who did attend was Israeli Prime Minister Benjamin Netanyahu, no stranger to intense security, who marched beside Hollande through the city streets. The highest ranking U.S. officials attending the march were Jane Hartley, the ambassador to France, and Victoria Nuland, the assistant secretary of state for European affairs. Attorney General Eric H. Holder Jr. was in Paris for meetings with law enforcement officials but did not participate in the march.\n\nKerry spent Sunday at a business summit hosted by India\'s prime minister, Narendra Modi. The United States is eager for India to relax stringent laws that function as barriers to foreign investment and hopes Modi\'s government will act to open the huge Indian market for more American businesses.\n\nIn a news conference, Kerry brushed aside criticism that the United States had not sent a more senior official to Paris as "quibbling a little bit." He noted that many staffers of the American Embassy in Paris attended the march, including the ambassador. He said he had wanted to be present at the march himself but could not because of his prior commitments in India.\n\n"But that is why I am going there on the way home, to make it crystal clear how passionately we feel about the events that have taken place there," he said.\n\n"And I don\'t think the people of France have any doubts about America\'s understanding of what happened, of our personal sense of loss and our deep commitment to the people of France in this moment of trauma.']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, datalistLabel[category]))

