import ast
from Variables import *

Lucavar_real = real_news_json
Lucavar_fake = fake_news_json


newreal = open(Lucavar_real, "w")
newfake = open(Lucavar_fake, "w")

with open(trainset_senza_duplicati,'r') as dataset:
    for line in dataset:
        article = ast.literal_eval(line)
        if article['label'] == "REAL" :
            newreal.write(line)
        else:
            newfake.write(line)

dataset.close()
newreal.close()
newfake.close()