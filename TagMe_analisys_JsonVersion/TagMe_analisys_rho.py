import urllib, json
from difflib import SequenceMatcher
from unidecode import unidecode
import ast

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

#Function that calculate the mean value of the most relevant word for the text
def tag_me_mean_value(text):
    #url = "https://tagme.d4science.org/tagme/tag?lang=en&tweet=true&gcube-token=edc123ea-fe22-48c0-90d1-3f8b11c82116-843339462&text= Recent poll show President Obama opening up a small lead over GOP rival Mitt Romney"
    #url = "https://tagme.d4science.org/tagme/tag?lang=en&include_abstract=true&include_categories=true&gcube-token=edc123ea-fe22-48c0-90d1-3f8b11c82116-843339462&text=Killing Obama administration rules, dismantling Obamacare and pushing through tax reform are on the early to-do list."
    url = "https://tagme.d4science.org/tagme/spot?lang=en&gcube-token=edc123ea-fe22-48c0-90d1-3f8b11c82116-843339462&tweet=true&text="+text+""
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    #print data
    a = data["annotations"]
    list1 = []
    for elem in a:
        if (elem["rho"] >= 0.6):
            # print elem["spot"]
            list1.append(str(elem["spot"]))

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
               # print '%10s %-10s  %f  %s' % (interest, keyword,
                #                              s.ratio(),
                 #                             '** MATCH **' if b else '')
                list.append(s.ratio())

        #print

   # print(list)
    if list != []:
        tot = 0
        for i in range(len(list)) :
            tot = tot + list[i]
    if list != []:
        media = tot/len(list)
        #print(media)
        return media
    else:
        return 0


mean_list = []
mean_list2 = []
cont = 0
totale=0
#Read each row of dataframe of real news and calculate mean value
with open("/home/luca/PycharmProjects/TagMe_analisys_JsonVersion/real.json",'r') as dataset:
    for line in dataset:
        article = ast.literal_eval(line)
        text = article['text']
        try:
            mean_list.append(tag_me_mean_value(remove_non_ascii(text)))
            #print("giusto %d" %cont)
            #mean_list.append(tag_me_mean_value(news.iloc[i].encode('ascii', 'ignore').decode('ascii')))
        except ValueError:
            print("sbagliato %d" %cont)
            # decoding failed
            totale = totale+1
        cont = cont+1

#print(mean_list)
#print(len(mean_list))

mean_real_news = 0

#mean function
def mean(list):
    sum = 0
    for i in range(len(list)):
        sum = sum + list[i]
    return sum

tot = mean(mean_list)

#Calculate global mean value of real_news file
mean_real_news = tot / len(mean_list)

cont2 = 0
totale2 = 0
#Read each row of dataframe of fake news and calculate mean value
with open("/home/luca/PycharmProjects/TagMe_analisys_JsonVersion/fake.json",'r') as dataset:
    for line in dataset:
        article = ast.literal_eval(line)
        text = article['text']
        try:
            mean_list2.append(tag_me_mean_value(remove_non_ascii(text)))
            #mean_list.append(tag_me_mean_value(news.iloc[i].encode('ascii', 'ignore').decode('ascii')))
        except ValueError:
            print(cont2)
            totale2 = totale2+1
            # decoding failed
        cont2 = cont2+1

print("Righe errate real news: %d" %totale)
print("Righe errate fake news: %d" %totale2)


mean_fake_news = 0
tot2 = mean(mean_list2)

#Calculate global mean value of fake_news file
mean_fake_news = tot2/len(mean_list2)

#Save output in a text file
with open('result_prova.txt', 'wb') as output:
    output.write("media similarita' real news: ")
    output.write(str(mean_real_news))
    output.write("\n")
    output.write("media similarita' fake news: ")
    output.write(str(mean_fake_news))