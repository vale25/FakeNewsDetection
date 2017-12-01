import urllib, json
#url = "https://tagme.d4science.org/tagme/tag?lang=en&tweet=true&gcube-token=edc123ea-fe22-48c0-90d1-3f8b11c82116-843339462&text= Recent poll show President Obama opening up a small lead over GOP rival Mitt Romney"
#url = "https://tagme.d4science.org/tagme/tag?lang=en&include_abstract=true&include_categories=true&gcube-token=edc123ea-fe22-48c0-90d1-3f8b11c82116-843339462&text=Schumacher won the race in Indianapolis"
url = "https://tagme.d4science.org/tagme/spot?lang=en&gcube-token=edc123ea-fe22-48c0-90d1-3f8b11c82116-843339462&tweet=true&text=Recent poll show President Obama opening up a small lead over GOP rival Mitt Romney"
response = urllib.urlopen(url)
data = json.loads(response.read())
a = data["spots"]
for elem in a:
    if(elem["lp"] >= 0.1):
        print elem["spot"]

#import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet

list1 = ['Ass','chair', 'Clinton']
#list2 = ['Fair', 'govern', 'happy']
list = []
cont = -1
appoggio = -1
for i in range(len(list1)):
    for j in range(i+1,len(list1)):
        wordFromList1 = wordnet.synsets(list1[i])
        wordFromList2 = wordnet.synsets(list1[j])
        if wordFromList1 and wordFromList2: #Thanks to @alexis' note
            s = wordFromList1[0].wup_similarity(wordFromList2[0])
            list.append(s)


print(list)



