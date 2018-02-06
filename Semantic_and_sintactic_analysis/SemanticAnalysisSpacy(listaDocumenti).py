#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
import spacy
from Variables import *
import ast
nlp = spacy.load('en')
SemanticSimDict = {}
contatore=0

notiziaAggiunta = "/home/luca/PycharmProjects/prova_json_notizieAggiunte.json"

cont = 0
docs = []
with open(RealJson_notiziaAggiunta,'r') as dataset:
    for line in dataset:
        if cont != 10:
            article = ast.literal_eval(line)
            text = article['text'].replace('\n', '')
            docs.append(nlp(unicode(text, errors='replace')))
            print(cont)
            cont+=1
print(docs)

for doc in docs:
    fakenews = nlp(u"1 Reply \nTyler Durden ? Perhaps the most beneficial outcome resulting from last night?s loss of the Clinton Clan, whose ?charitable? donations from generous donors such as Saudi Arabia to the Clinton Foundation just ended, is that with Hillary not in charge, the probability of World War III has been taken off the table. \nThis was confirmed early this morning, When Russian President Vladimir Putin ? whose relations with the US and Barack Obama have deteriorated to Cold War levels ? congratulated Donald Trump for his election victory on Wednesday, and said he expected relations between the Kremlin and Washington to improve. \nThe Kremlin announced that Putin had sent a telegram to Trump on Wednesday morning expressing ? his hope they can work together toward the end of the crisis in Russian-American relations, as well address the pressing issues of the international agenda and the search for effective responses to global security challenges .? \nAdditionally, speaking at the presentation ceremony of foreign ambassadors? letters of credentials in Moscow, President Putin said that Russia is ready and looks forward to restoring bilateral relations with the United States, Russian President Vladimir Putin said, commenting on the news of Donald Trump?s victory in the US presidential election. \n?We heard Trump?s campaign rhetoric while still a candidate for the US presidency, which was focused on restoring the relations between Russia and the United States.? \nHe added that ?we understand and are aware that it will be a difficult path in the light of the degradation in which, unfortunately, the relationship between Russia and the US are at the moment.? \nSpeaking about the degraded state of relations between the countries, the Russian president once again stressed that ?it is not our fault that Russia-US relations are as you see them.? \nOther Russian politicians joined in. \nRussian State Duma Speaker Vyacheslav Volodin has also expressed hope that Trump?s victory in the presidential election will help pave the way for a more constructive dialogue between Moscow and Washington. \n?The current US-Russian relations cannot be called friendly. Hopefully, with the new US president a more constructive dialogue will be possible between our countries,? he said. ?The Russian Parliament will welcome and support any steps in this direction,? Volodin added on Wednesday. \nCommenting on Donald Trump?s victory in the US presidential election, Russian Foreign Minister Sergey Lavrov said Russia will judge the new US administration by its actions and take appropriate steps in response. ?We are ready to work with any US leader elected by the US people,? the minister said on Wednesday. \n?I can?t say that all the previous US leaders were always predictable. This is life, this is politics. I have heard many words but we will judge by actions.? \nSergey Zheleznyak, member of Russian President Vladimir Putin?s United Russia party in parliament, hailed Trump?s ?deserved victory? in a statement on the party?s website. \n?Despite all the intrigues and provocations that the current U.S. government put in front of Trump, people supported his intention to address the serious problems that have accumulated in America, and to move from confrontation to cooperation with Russia and the world, ? Zheleznyak said. ?I hope that between now and [his] entry into office as the new president of the United States there will be no tragic events and the new U.S. administration will have enough political will and wisdom for civilized solutions to existing problems.? \nRussia?s second biggest party the Communist Party also issued a statement Wednesday morning, expressing hope for more cooperation and calling Trump?s win ?astounding? and against the ?elite clans? in the United States. The party leader was more lukewarm on the news, noting that U.S. imperialism was unlikely to change. \nVladimir Zhirinovsky, the right-wing nationalist leader of the Liberal Democratic Party who has previously been nicknamed the Russian Donald Trump, called Clinton a ?mindless old woman? and praised U.S. voters for ?coming to their senses? after eight years of President Barack Obama, whom he referred to as ?the Afro-American.? SF Source Zerohedge  ")
    SemanticSimDict[contatore] = doc.similarity(fakenews)
    print(doc.similarity(fakenews))
    contatore+=1


contatore2=0
print SemanticSimDict
lineTextReal = ""
sortedSemantic = sorted(SemanticSimDict.items(), key=lambda x: x[1])
sortedSemantic.reverse()
print(sortedSemantic)
maxSim = sortedSemantic[0][0]
print(maxSim)
with open(RealJson_notiziaAggiunta, 'r') as dataset:
    for line in dataset:
        if contatore2 == maxSim:
            article = ast.literal_eval(line)
            lineTextReal = article['text'].replace('\n', '')
        contatore2+=1
print("Fake news inserita: \n")
print(str(fakenews))
print("\n Real news corrispondente: \n")
print(lineTextReal)