import urllib, json
from difflib import SequenceMatcher

#text = "Recent poll show President Obama opening up a small lead over GOP rival Mitt Romney"

#Function that calculate the mean value of the most relevant word for the text
def tag_me_mean_value(text):
    #url = "https://tagme.d4science.org/tagme/tag?lang=en&tweet=true&gcube-token=edc123ea-fe22-48c0-90d1-3f8b11c82116-843339462&text= Recent poll show President Obama opening up a small lead over GOP rival Mitt Romney"
    #url = "https://tagme.d4science.org/tagme/tag?lang=en&include_abstract=true&include_categories=true&gcube-token=edc123ea-fe22-48c0-90d1-3f8b11c82116-843339462&text=Killing Obama administration rules, dismantling Obamacare and pushing through tax reform are on the early to-do list."
    url = "https://tagme.d4science.org/tagme/spot?lang=en&gcube-token=edc123ea-fe22-48c0-90d1-3f8b11c82116-843339462&tweet=true&text="+text+""
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    #print data
    a = data["spots"]
    list1 = []
    for elem in a:
        if(elem["lp"] >= 0.1):
            #print elem["spot"]
            list1.append(str(elem["spot"]))

    '''
    #import nltk
    #nltk.download('wordnet')
    from nltk.corpus import wordnet
    print(list1)
    list = []
    cont = -1
    appoggio = -1
    for i in range(len(list1)):
        for j in range(i+1,len(list1)):
            wordFromList1 = wordnet.synsets(list1[i])
            wordFromList2 = wordnet.synsets(list1[j])
            if wordFromList1 and wordFromList2: #Thanks to @alexis' note
                s = wordFromList1[0].wup_similarity(wordFromList2[0])
                list.append(s)'''

    list = []
    s = SequenceMatcher(None)

    limit = 0.50

    for i in range(len(list1)):
        interest = list1[i]
        s.set_seq2(interest)
        for j in range(i+1,len(list1)):
            keyword = list1[j]
            s.set_seq1(keyword)
            if interest != keyword:
                b = s.ratio()>=limit and len(s.get_matching_blocks())==2
                print '%10s %-10s  %f  %s' % (interest, keyword,
                                              s.ratio(),
                                              '** MATCH **' if b else '')
                list.append(s.ratio())

        print

    print(list)
    if list != []:
        tot = 0
        for i in range(len(list)) :
            tot = tot + list[i]
    if list != []:
        media = tot/len(list)
        print(media)
        return media
    else:
        return 0


mean_list = []
mean_list2 = []
'''for i in range(2):
    mean_list.append(tag_me_mean_value(text))

print(mean_list)'''

'''
#Read each line of the csv file and create the list of mean_values
import csv
f = open('realnews_csv', 'rb')
reader = csv.reader(f)
cont = 1
for row in reader:
    if cont != 0:
        cont = cont-1
        print(row)
        if row != []:
            try:
                mean_list.append(tag_me_mean_value(str(row)))
            except ValueError:
                # decoding failed
                continue
f.close()
'''
import pickle
with open("real_news", "rb") as f:
    news = pickle.load(f)

for i in range(len(news)):
    print(news.iloc[i])
    print(i)
    try:
        mean_list.append(tag_me_mean_value(news.iloc[i].encode('ascii', 'ignore').decode('ascii')))
    except ValueError:
        # decoding failed
        continue



print(mean_list)
print(len(mean_list))

mean_real_news = 0
def mean(list):
    sum = 0
    for i in range(len(list)):
        sum = sum + list[i]
    return sum

tot = mean(mean_list)

mean_real_news = tot / len(mean_list)

with open("fake_news", "rb") as f:
    news = pickle.load(f)

for i in range(len(news)):
    print(news.iloc[i])
    print(i)
    try:
        mean_list2.append(tag_me_mean_value(news.iloc[i].encode('ascii', 'ignore').decode('ascii')))
    except ValueError:
        # decoding failed
        continue

mean_fake_news = 0
tot2 = mean(mean_list2)
mean_fake_news = tot2/len(mean_list2)
print("media similarita' real news: ")
print(mean_real_news)
print("media similarita' fake news: ")
print(mean_fake_news)


with open('result.txt', 'wb') as output:
    output.write("media similarita' real news: ")
    output.write(str(mean_real_news))
    output.write("\n")
    output.write("media similarita' fake news: ")
    output.write(str(mean_fake_news))