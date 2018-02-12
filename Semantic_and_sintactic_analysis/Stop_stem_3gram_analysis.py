#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
from nltk.util import ngrams
from Variables import *
import ast
from nltk.stem import PorterStemmer
import nltk
from nltk.corpus import stopwords
import re
from itertools import chain
from nltk.corpus import wordnet

#QUESTA CLASSE HA FUNZIONATO DOVE L'ANALISI SINTATTICA DI COSINESIMANALISYSNEWS HA FALLITO

fake = "Thursday, 27 October 2016 Biden and Trump to Duel \nSeeking to duplicate, if not surpass, the famous duel between Vice President Aaron Burr and Treasury Secretary Alexander Hamilton, Republican candidate for president, Donald Trump, and Vice President Joe Biden, agreed to fight a pistol duel. Although details of the duel have yet to be finalized, Amiko Aventurista, reports the duel will likely take place on the eve of the election. \nThree independent sources confirmed negotiations over broadcast rights are extremely tense. Trump demands the duel be the inaugural show of his new venture, Trump TV. \"It was my idea. I was the one who said I could shot someone on Fifth Avenue and my supporters would be with me. Other than Hilary, Obama, Rubio, Cruz, Jeb Bush, and a ton of others, I can think of no one better to shot than hair plug Joe. I'm the greatest shooter ever. A real sniper.\" \nBiden insist MSNBC must be the broadcaster because its liberal and minority audience wants to see Trump with several gun shots. In a response to Trump, Biden said, \"There is no way I can miss. His hair glows bright orange. All I have to do is point toward the glow\". \nMegan Kelly of Fox says Fox must host the show because she wants to see \"blood\" coming everywhere out of Trump just like he said blood was coming out of her. CNN's Wolf Blitzer decline to comment. Even ESPN is making a play for the event, pointing out it regularly shows non-traditional sporting events, such as bull riding, cross bow, and bowling. \nBoth sides agree Lin Manuel Mirada, producer of the hit Broadway show, Alexander Hamilton, should direct the event. Manuel Mirada said, \"I would be honored to produce the event. I know my smash Broadway hit, Hamilton, is only a show about a duel not a real duet but I think that experience qualifies me to produce a show about a real duel. After all, the only difference is the guns are real.\" \nThe National Rifle Association (NRA) has agreed to fully pay for and sponsor the event. NRA President Wayne LaPierre release the following statement, \"Finally we have bi-partisan agreement. I should have thought of this first\". Make Amiko Aventurista's  ".replace('\n', '')
#fake = "We Are Change \nDonald Trump on Saturday was quickly ushered off the stage by Secret Service agents in the middle of a campaign speech in Nevada after an incident in the crowd near the front of the stage.\nSecret Service rushes Trump off stage at Reno rally https://t.co/n82d9jXopX \n? Chrissy (@omgitsmechrissy) November 6, 2016 \nVideo shows that Trump was in the middle of his speech when the incident occurred. He was looking into the crowd, his hand over his eyes to block the glare from the stage lights, when Secret Service agents grabbed him and escorted him off the stage. Trump ducked his head as he left the stage. The crowd panicked with frightened looks on their faces, as the Secret Service and police tactical units rushed in to quickly arrest the man. Video on twitter shows the moment that the Secret Service and law enforcement took down the man. Got footage of man who was detained by police and Secret Service after @realDonaldTrump was rushed off stage by USSS agents pic.twitter.com/FVEieSYj5w \n? Jeremy Diamond (@JDiamond1) November 6, 2016 \nEarly unconfirmed reports suggest a man was armed in the crowd according to some witnesses. One witness said that they were in the crowd when an unknown guy creeped toward the stage staring at Trump. The witness then proceeded to get the attention of four bigger guys surrounding them and confronted the man. The man then freaked out and reached into his pocket to grab what looked like a gun.? According to the witness the man was mumbling about ?the delegates.? ? I was in the crowd, me and my dad saw a guy creeping toward the stage staring at trump. i got the attention of 4 big guys around me and we confronted him and when we did he spurged out and reached into his pocket to grab what looked like a gun. when we tackled him to the ground and between punches he kept saying something about ?the delegates?? he must have the delegates. sorry i?m pretty shaken up right now. ? With one person in the crowd shouting ?he?s got a gun.? The man was then detained by police officers, Secret Service agents and SWAT armed with assault rifles and taken to a side room for questioning. The suspect is seen below. Trump returned to the stage minutes later and proceeded to continue his speech before thanking the Secret Service and police. ?Nobody said it was going to be easy for us, but we will never be stopped. We will never be stopped. I want to thank the Secret Service. These guys are fantastic.? \n~Donald Trump, said.\nLuke breaks down the details in the video below of the attempted assassination of the anti-establishment candidate Donald Trump.\nIt?s worth noting that the last Trump assassination attempt also occurred in Nevada when Michael Sandford a British citizen attempted to grab a police officer?s gun and shoot Donald Trump a few weeks ago.\nJulian Assange was right when he said earlier today to John Pilger that ?anti-establishment Trump Wouldn?t Be Allowed To Win.? Although Julian just missed how he would be stopped.\n(THIS IS A DEVELOPING STORY AND WILL BE UPDATED AS NEW DETAILS BECOME AVAILABLE.) The post #BREAKING: SECOND Assassination Attempt On Trump In NV; Suspect Detained (LIVE BLOG) appeared first on We Are Change .".replace('\n','')
#real = "U.S. Secretary of State John F. Kerry said Monday that he will stop in Paris later this week, amid criticism that no top American officials attended Sunday?s unity march against terrorism.\n\nKerry said he expects to arrive in Paris Thursday evening, as he heads home after a week abroad. He said he will fly to France at the conclusion of a series of meetings scheduled for Thursday in Sofia, Bulgaria. He plans to meet the next day with Foreign Minister Laurent Fabius and President Francois Hollande, then return to Washington.\n\nThe visit by Kerry, who has family and childhood ties to the country and speaks fluent French, could address some of the criticism that the United States snubbed France in its darkest hour in many years.\n\nThe French press on Monday was filled with questions about why neither President Obama nor Kerry attended Sunday?s march, as about 40 leaders of other nations did. Obama was said to have stayed away because his own security needs can be taxing on a country, and Kerry had prior commitments.\n\nAmong roughly 40 leaders who did attend was Israeli Prime Minister Benjamin Netanyahu, no stranger to intense security, who marched beside Hollande through the city streets. The highest ranking U.S. officials attending the march were Jane Hartley, the ambassador to France, and Victoria Nuland, the assistant secretary of state for European affairs. Attorney General Eric H. Holder Jr. was in Paris for meetings with law enforcement officials but did not participate in the march.\n\nKerry spent Sunday at a business summit hosted by India?s prime minister, Narendra Modi. The United States is eager for India to relax stringent laws that function as barriers to foreign investment and hopes Modi?s government will act to open the huge Indian market for more American businesses.\n\nIn a news conference, Kerry brushed aside criticism that the United States had not sent a more senior official to Paris as ?quibbling a little bit.? He noted that many staffers of the American Embassy in Paris attended the march, including the ambassador. He said he had wanted to be present at the march himself but could not because of his prior commitments in India.\n\n?But that is why I am going there on the way home, to make it crystal clear how passionately we feel about the events that have taken place there,? he said.\n\n?And I don?t think the people of France have any doubts about America?s understanding of what happened, of our personal sense of loss and our deep commitment to the people of France in this moment of trauma.?"

#Effettua lo stopping, eliminando le parole comuni prive di significato
stopwords_en = set(stopwords.words('english'))

sents = nltk.sent_tokenize(fake)

sents_rm_stopwords = []
for sent in sents:
    sents_rm_stopwords.append(' '.join(w for w in nltk.word_tokenize(sent) if w.lower() not in stopwords_en))

fakestr1 = "".join(sents_rm_stopwords)
fakestr = re.sub(r'[^\w\s]','',fakestr1)
fakestr = [re.sub(' +',' ',fakestr)]
#print("stopping:")
#print(fakestr)

#Effettua lo stemming delle parole della notizia
ps = PorterStemmer()
final = [" ".join([ps.stem(token) for token in sentence.split(" ")]) for sentence in fakestr]
fakestrfinal = "".join(final)
#print("stemming:")
#print(fakestrfinal)


#Effettua la divisione del testo in trigrammi
n = 3
trigramsFake = list(ngrams(fakestrfinal.lower().split(), n))
#trigramsReal = list(ngrams(real.lower().split(), n))
#print(list(trigramsReal))
t3 = "I love to fight Biden and i want to make me feel better"
t4 = "I like to i want to fight Biden and my house is me feel better"
t5 = list(ngrams(t3.lower().split(), n))
t6 = list(ngrams(t4.lower().split(), n))

#Funzione che oltre a verificare che i trigrammi sono comuni trova anche le parole sinonime e verifica che ci sia uguaglianza
def compare(trigrams1, trigrams2):
   common=[]
   comuni=0
   for grams1 in trigrams1:
        if grams1 in trigrams2:
            common.append(grams1)
            comuni+=1
   return comuni,common
  # return comuni

def compareWithSynonyms(trigrams1,trigrams2):
    cont = 0
    comuni = 0
    commons = 0
    list_comuni = []
    for elem in trigrams1:
        #print(elem[2])
        for elem2 in trigrams2:
            #print(elem2[0])
            for i in range(3):
                if(elem[i] != elem2[i]):
                    synonyms = wordnet.synsets(elem2[i])
                    lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
                    #print(lemmas)
                    for element in lemmas:
                        if(elem[i] == element):
                            comuni+=1
                else:
                    comuni+=1
                cont + 1
            #print comuni
            if comuni == 3:
                commons+=1
                a = [(elem2[0],elem2[1],elem2[2])]
                list_comuni.append(a)
                comuni = 0
            else:
                comuni = 0

    return commons,list_comuni


#a = compareWithSynonyms(t5,t6)
#print(a)


#result = compare(trigramsFake, trigramsFake)
#print(result)

cont=0
contatore =0
trigramsDict = {}
with open(RealJson_notiziaAggiunta, 'r') as dataset:
    for line in dataset:
        if cont != 300:
            article = ast.literal_eval(line)
            lineReal = article['text'].replace('\n', '')
            lineReal2 = lineReal.decode('utf8').encode('ascii', errors='ignore')

            #Effettua lo stopping della real news
            stopwords_en = set(stopwords.words('english'))
            sents = nltk.sent_tokenize(lineReal2)

            sents_rm_stopwords2 = []
            for sent in sents:
                sents_rm_stopwords2.append(' '.join(w for w in nltk.word_tokenize(sent) if w.lower() not in stopwords_en))

            realstrfinal1 = "".join(sents_rm_stopwords2)
            realstrfinal = re.sub(r'[^\w\s]', '', realstrfinal1)
            realstrfinal = [re.sub(' +', ' ', realstrfinal)]

            # Effettua lo stemming della real news
            ps = PorterStemmer()
            final = [" ".join([ps.stem(token) for token in sentence.split(" ")]) for sentence in realstrfinal]
            realstrfinal = "".join(final)

            #print(realstrfinal)

            #Dividi la real news in trigrammi
            trigramsReal = list(ngrams(realstrfinal.lower().split(), n))

            #Compara i trigrammi real e fake e salva i risultati della comparazione nel dizionario
            result = compare(trigramsFake,trigramsReal)
            trigramsDict[cont] = result
            print(cont)
            cont+=1

print(trigramsDict)
sortedNgrams = sorted(trigramsDict.items(), key=lambda x: x[1])
sortedNgrams.reverse()
print("Lista ordinata numero maggiore ngrammi comuni:")
print(sortedNgrams)
maxNgram = sortedNgrams[0][0]
print(maxNgram)

lineTextReal = ""

print("Fake news inserita: \n")
print(fake)
print("\n---------------------------------------------------------------------------------")

#Ricerca nel dataset della news real corrispondente
with open(RealJson_notiziaAggiunta, 'r') as dataset:
    for line in dataset:
        if contatore == maxNgram:
            article = ast.literal_eval(line)
            lineTextReal = article['text'].replace('\n', '')
            titleReal = article['title'].replace('\n', '')
            print("\n Real news corrispondente con numero maggiore di Ngrammi comuni: \n")
            print("titolo:\n")
            print(titleReal)
            print("\nTesto della news:\n")
            print(lineTextReal)
        contatore+=1


