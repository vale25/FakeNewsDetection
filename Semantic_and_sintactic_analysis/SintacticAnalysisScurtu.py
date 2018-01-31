#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
import urllib,urllib2
import json
from Variables import *
import ast

contatore = 0
contatore2 = 0
similarityDict = {}
SemanticSimDict = {}
API_URL="http://www.scurtu.it/apis/documentSimilarity"
inputDict={}

#notizia fake inserita
#fake = "1 Reply \nTyler Durden ? Perhaps the most beneficial outcome resulting from last night?s loss of the Clinton Clan, whose ?charitable? donations from generous donors such as Saudi Arabia to the Clinton Foundation just ended, is that with Hillary not in charge, the probability of World War III has been taken off the table. \nThis was confirmed early this morning, When Russian President Vladimir Putin ? whose relations with the US and Barack Obama have deteriorated to Cold War levels ? congratulated Donald Trump for his election victory on Wednesday, and said he expected relations between the Kremlin and Washington to improve. \nThe Kremlin announced that Putin had sent a telegram to Trump on Wednesday morning expressing ? his hope they can work together toward the end of the crisis in Russian-American relations, as well address the pressing issues of the international agenda and the search for effective responses to global security challenges .? \nAdditionally, speaking at the presentation ceremony of foreign ambassadors? letters of credentials in Moscow, President Putin said that Russia is ready and looks forward to restoring bilateral relations with the United States, Russian President Vladimir Putin said, commenting on the news of Donald Trump?s victory in the US presidential election. \n?We heard Trump?s campaign rhetoric while still a candidate for the US presidency, which was focused on restoring the relations between Russia and the United States.? \nHe added that ?we understand and are aware that it will be a difficult path in the light of the degradation in which, unfortunately, the relationship between Russia and the US are at the moment.? \nSpeaking about the degraded state of relations between the countries, the Russian president once again stressed that ?it is not our fault that Russia-US relations are as you see them.? \nOther Russian politicians joined in. \nRussian State Duma Speaker Vyacheslav Volodin has also expressed hope that Trump?s victory in the presidential election will help pave the way for a more constructive dialogue between Moscow and Washington. \n?The current US-Russian relations cannot be called friendly. Hopefully, with the new US president a more constructive dialogue will be possible between our countries,? he said. ?The Russian Parliament will welcome and support any steps in this direction,? Volodin added on Wednesday. \nCommenting on Donald Trump?s victory in the US presidential election, Russian Foreign Minister Sergey Lavrov said Russia will judge the new US administration by its actions and take appropriate steps in response. ?We are ready to work with any US leader elected by the US people,? the minister said on Wednesday. \n?I can?t say that all the previous US leaders were always predictable. This is life, this is politics. I have heard many words but we will judge by actions.? \nSergey Zheleznyak, member of Russian President Vladimir Putin?s United Russia party in parliament, hailed Trump?s ?deserved victory? in a statement on the party?s website. \n?Despite all the intrigues and provocations that the current U.S. government put in front of Trump, people supported his intention to address the serious problems that have accumulated in America, and to move from confrontation to cooperation with Russia and the world, ? Zheleznyak said. ?I hope that between now and [his] entry into office as the new president of the United States there will be no tragic events and the new U.S. administration will have enough political will and wisdom for civilized solutions to existing problems.? \nRussia?s second biggest party the Communist Party also issued a statement Wednesday morning, expressing hope for more cooperation and calling Trump?s win ?astounding? and against the ?elite clans? in the United States. The party leader was more lukewarm on the news, noting that U.S. imperialism was unlikely to change. \nVladimir Zhirinovsky, the right-wing nationalist leader of the Liberal Democratic Party who has previously been nicknamed the Russian Donald Trump, called Clinton a ?mindless old woman? and praised U.S. voters for ?coming to their senses? after eight years of President Barack Obama, whom he referred to as ?the Afro-American.? SF Source Zerohedge  ".replace('\n', '')
#fake = "(Before It's News)\nIvanka Trump is going to have to back off from her father’s campaign, because the hateful and sexist rhetoric of Donald Trump is severely hurting Ivanka’s clothing and lifestyle brand.\nWomen are turning on Ivanka Trump as she continues supporting her father despite allegations of sexual harassment against him and a 2005 audio tape capturing him bragging in lewd terms that he can do whatever he wants to women.\nNow, the growing group of women are boycotting her line of clothing, jewelry, perfume and accessories sold as part of the Ivanka Trump Collection. They are also calling on the stores that carry the brand, including Nordstrom, Bloomingdale’s and Macy’s, to stop selling it.\nIt has even created its own hashtag, #Ivankant, as well as #GrabYourWallet.\nFrom The Daily Mail :\n‘If Ivanka Trump had distanced herself from the campaign I would not be boycotting her,’ Shannon Coulter, who called on Americans to boycott the brand earlier this month, told the Guardian.\n‘But something changed for me when that tape was released.’\nCoulter, who shared her own experience of sexual harassment at the hands of a male superior, launched the hashtag ‘GrabYourWallet’ on October 11, a reference to Trump’s offensive ‘grab them by the p***y’ remark from the audio tape.\nThe problem obviously for Ivanka, is that Donald Trump’s base, for the most part, doesn’t shop at Bloomingdale’s or Nordstrom, which are two of the largest stores that carry her clothing line, along with Macy’s.\nWhat are your thoughts, should Ivanka’s business be hurt because of the actions of her father?\nFrom Politico:\nThe New York Times cited a deposition from a woman who claimed that Donald Trump groped her under the table decades ago, but the presumptive Republican presidential nominee is certainly not a groper, his daughter said Wednesday.\n“Look, I’m not in every interaction my father has, but he’s not a groper,” Ivanka Trump said in an interview broadcast Wednesday on “CBS This Morning.” “It’s not who he is. And I’ve known my father obviously my whole life and he has total respect for women.”\nThe billionaire businessman launched a Twitter salvo the “failing” newspaper for its “false, malicious & libelous story,” catapulting the story to become the newspaper’s most popular of the year, according to assistant news editor Theodore Kim.\n—\nIvanka Trump said she read the Sunday cover story and “found it to be pretty disturbing, based on the facts as I know them, and obviously I very much know them” as a daughter and an executive who’s worked alongside him for more than a decade.\n“I was bothered by it, but it’s largely been discredited since,” she said, referring to Brewer Lane’s criticism of the report. Brewer Lane, the ex-girlfriend whose first run-in with Donald Trump was used as the lead anecdote for the article, titled “Crossing the Line: How Donald Trump Behaved With Women in Private,” accused the newspaper of putting a negative connotation on her words.\n“Most of the time when stories are inaccurate they’re not discredited, and I will be frustrated by that, but in this case I think they went so far,” Ivanka Trump continued. “They had such a strong thesis and created facts to reinforce it and, you know, I think that narrative has been playing out now and there’s backlash in that regard.”\nSource RealTimePolitics.com Check out more contributions by Jeffery Pritchett ranging from UFO to Bigfoot to Paranormal to Prophecy".replace('\n', '').replace('\n', '')
#fake = "We Are Change \nDonald Trump on Saturday was quickly ushered off the stage by Secret Service agents in the middle of a campaign speech in Nevada after an incident in the crowd near the front of the stage.\nSecret Service rushes Trump off stage at Reno rally https://t.co/n82d9jXopX \n? Chrissy (@omgitsmechrissy) November 6, 2016 \nVideo shows that Trump was in the middle of his speech when the incident occurred. He was looking into the crowd, his hand over his eyes to block the glare from the stage lights, when Secret Service agents grabbed him and escorted him off the stage. Trump ducked his head as he left the stage. The crowd panicked with frightened looks on their faces, as the Secret Service and police tactical units rushed in to quickly arrest the man. Video on twitter shows the moment that the Secret Service and law enforcement took down the man. Got footage of man who was detained by police and Secret Service after @realDonaldTrump was rushed off stage by USSS agents pic.twitter.com/FVEieSYj5w \n? Jeremy Diamond (@JDiamond1) November 6, 2016 \nEarly unconfirmed reports suggest a man was armed in the crowd according to some witnesses. One witness said that they were in the crowd when an unknown guy creeped toward the stage staring at Trump. The witness then proceeded to get the attention of four bigger guys surrounding them and confronted the man. The man then freaked out and reached into his pocket to grab what looked like a gun.? According to the witness the man was mumbling about ?the delegates.? ? I was in the crowd, me and my dad saw a guy creeping toward the stage staring at trump. i got the attention of 4 big guys around me and we confronted him and when we did he spurged out and reached into his pocket to grab what looked like a gun. when we tackled him to the ground and between punches he kept saying something about ?the delegates?? he must have the delegates. sorry i?m pretty shaken up right now. ? With one person in the crowd shouting ?he?s got a gun.? The man was then detained by police officers, Secret Service agents and SWAT armed with assault rifles and taken to a side room for questioning. The suspect is seen below. Trump returned to the stage minutes later and proceeded to continue his speech before thanking the Secret Service and police. ?Nobody said it was going to be easy for us, but we will never be stopped. We will never be stopped. I want to thank the Secret Service. These guys are fantastic.? \n~Donald Trump, said.\nLuke breaks down the details in the video below of the attempted assassination of the anti-establishment candidate Donald Trump.\nIt?s worth noting that the last Trump assassination attempt also occurred in Nevada when Michael Sandford a British citizen attempted to grab a police officer?s gun and shoot Donald Trump a few weeks ago.\nJulian Assange was right when he said earlier today to John Pilger that ?anti-establishment Trump Wouldn?t Be Allowed To Win.? Although Julian just missed how he would be stopped.\n(THIS IS A DEVELOPING STORY AND WILL BE UPDATED AS NEW DETAILS BECOME AVAILABLE.) The post #BREAKING: SECOND Assassination Attempt On Trump In NV; Suspect Detained (LIVE BLOG) appeared first on We Are Change .".replace('\n', '')
fake = "Thursday, 27 October 2016 Biden and Trump to Duel \nSeeking to duplicate, if not surpass, the famous duel between Vice President Aaron Burr and Treasury Secretary Alexander Hamilton, Republican candidate for president, Donald Trump, and Vice President Joe Biden, agreed to fight a pistol duel. Although details of the duel have yet to be finalized, Amiko Aventurista, reports the duel will likely take place on the eve of the election. \nThree independent sources confirmed negotiations over broadcast rights are extremely tense. Trump demands the duel be the inaugural show of his new venture, Trump TV. \"It was my idea. I was the one who said I could shot someone on Fifth Avenue and my supporters would be with me. Other than Hilary, Obama, Rubio, Cruz, Jeb Bush, and a ton of others, I can think of no one better to shot than hair plug Joe. I'm the greatest shooter ever. A real sniper.\" \nBiden insist MSNBC must be the broadcaster because its liberal and minority audience wants to see Trump with several gun shots. In a response to Trump, Biden said, \"There is no way I can miss. His hair glows bright orange. All I have to do is point toward the glow\". \nMegan Kelly of Fox says Fox must host the show because she wants to see \"blood\" coming everywhere out of Trump just like he said blood was coming out of her. CNN's Wolf Blitzer decline to comment. Even ESPN is making a play for the event, pointing out it regularly shows non-traditional sporting events, such as bull riding, cross bow, and bowling. \nBoth sides agree Lin Manuel Mirada, producer of the hit Broadway show, Alexander Hamilton, should direct the event. Manuel Mirada said, \"I would be honored to produce the event. I know my smash Broadway hit, Hamilton, is only a show about a duel not a real duet but I think that experience qualifies me to produce a show about a real duel. After all, the only difference is the guns are real.\" \nThe National Rifle Association (NRA) has agreed to fully pay for and sponsor the event. NRA President Wayne LaPierre release the following statement, \"Finally we have bi-partisan agreement. I should have thought of this first\". Make Amiko Aventurista's  ".replace('\n', '')

#Aggiunta della notizia fake nel dizionario per il calcolo della similarità
inputDict['doc1']=fake

#Effettua il calcolo della similarità semantica e sintattica e salva il contenuto nei corrispettivi dizionari
with open(RealJson_notiziaAggiunta,'r') as dataset:
    for line in dataset:
        #if contatore != 10:  #decommenta questa line per solo 10 iterazioni
            article = ast.literal_eval(line)
            text = article['text'].replace('\n', '')
            inputDict['doc2'] = text

            #calcolo similarità sintattica(coseno similarità) da tool esterno
            params = urllib.urlencode(inputDict)
            f = urllib2.urlopen(API_URL, params)
            response= f.read()
            responseObject=json.loads(response)
            similarityDict[contatore] = responseObject['result']
            contatore+=1

            #stampa i risultati di similarità ottenuti
            print responseObject['result']

#print similarityDict

#Ordina le coppie chiave-valore dal più alto al più basso in base al valore
sorted = sorted(similarityDict.items(), key=lambda x: x[1])
sorted.reverse()
print("Lista ordinata similarita' sintattica:")
print(sorted)

#Taglia ai primi 20 elementi significativi
'''top20Sintact = sorted[:20]
print("Lista tagliata:")
print top20Sintact'''

maxSintactic = sorted[0][0]
print(maxSintactic)

lineTextReal = ""

print("Fake news inserita: \n")
print(fake)

#Ricerca nel dataset della news real corrispondente
with open(RealJson_notiziaAggiunta, 'r') as dataset:
    for line in dataset:
        if contatore2 == maxSintactic:
            article = ast.literal_eval(line)
            lineTextReal = article['text'].replace('\n', '')
            print("\n Real news corrispondente con valore sintattico piu' alto: \n")
            print(lineTextReal)
        contatore2+=1
