#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys
from gensim.models import doc2vec
from collections import namedtuple

# Load data
text1 = " Parts Of Patriot Act Expire, Even As Senate Moves On Bill Limiting SurveillanceIt was a dramatic day on the floor of the United States Senate on Sunday. Unable to overcome parliamentary maneuvers by Sen. Rand Paul, the body adjourned and let three controversial provisions of the Patriot Act expire at midnight.Trying to beat a midnight deadline during a rare Sunday session, Senate Majority Leader Mitch McConnell tried to fast track a House bill that would overhaul the government's bulk collection of Americans' phone records.At around 7 p.m. ET, the House bill cleared a key procedural hurdle, but as the sun set on Washington, it became clear that a Senate rule allowing for 30 hours of debate would force parts of the Patriot Act to expire at least temporarily.The Patriot Act will expire tonight, Paul, the Kentucky Republican who has led the charge against the government's bulk collection program, said. But it will only be temporary. They will ultimately get their way.Before this session, Paul promised to use any parliamentary moves available to him to force any Senate vote on the measure to happen after the 12 a.m. deadline.He was warned by lawmakers on both sides of the aisle that he was putting the country at risk.To go dark on this is a risk on Americans' lives."
text2 = "Washington (CNN) The Republican Party is waking up -- but it might already be too late.Donald Trump's stroll toward the GOP presidential nomination is starting to turn the denial evident for months among key party power brokers to desperation. The mood of some in the party was aptly summed up Thursday by Republican lobbyist and former congressman Vin Weber on CNN's The Lead with Jake Tapper.All of a sudden, everybody is saying 'Oh My God ? the house is burning down we should have done something before it got this far,' said Weber, who is supporting John Kasich in the presidential race and is calling on the party to unite behind the Ohio Governor.Sen. Marco Rubio, who pulled out of the presidential race on Tuesday after failing to take down Trump, had a grim assessment of the Republican Party's state of play on his first day back at work in the Senate on Thursday.Hopefully there's time to still prevent a Trump nomination."
text3 = "With the Democratic presidential primary in its twilight, frustration within the ranks over the party's handling of the primary process spilled out this week as Bernie Sanders supporters lashed out at party leaders, arguing that their candidate has been treated unfairly. on Wednesday afternoon, Vice President Joe Biden said if such disruption happens again, He's going to have to be more aggressive in speaking out about it.""But here we are in May, as was pointed out,Biden continued. Hillary was still in this in May, in June. I'm confident that Bernie will be supportive if Hillary wins, which the numbers indicate will happen. So I'm not worried. There's no fundamental split in the Democratic Party.Leading congressional Democrats also pushed Sanders to rein in his supporters."
doc1 = [text1, text2, text3]

# Transform data (you can add more data preprocessing steps)

docs = []
analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
for i, text in enumerate(doc1):
    words = text.lower().split()
    tags = [i]
    docs.append(analyzedDocument(words, tags))

# Train model

model = doc2vec.Doc2Vec(docs, size = 1000, window = 300, min_count = 1, workers = 4)


tokens = "Thursday, 27 October 2016 Biden and Trump to Duel Seeking to duplicate, if not surpass, the famous duel between Vice President Aaron Burr and Treasury Secretary Alexander Hamilton, Republican candidate for president, Donald Trump, and Vice President Joe Biden, agreed to fight a pistol duel. Although details of the duel have yet to be finalized, Amiko Aventurista, reports the duel will likely take place on the eve of the election. Three independent sources confirmed negotiations over broadcast rights are extremely tense. Trump demands the duel be the inaugural show of his new venture, Trump TV. It was my idea. I was the one who said I could shot someone on Fifth Avenue and my supporters would be with me. Other than Hilary, Obama, Rubio, Cruz, Jeb Bush, and a ton of others, I can think of no one better to shot than hair plug Joe. I'm the greatest shooter ever. A real sniper. Biden insist MSNBC must be the broadcaster because its liberal and minority audience wants to see Trump with several gun shots."
new_vector = model.infer_vector(tokens)
sims = model.docvecs.most_similar([new_vector])
print sims