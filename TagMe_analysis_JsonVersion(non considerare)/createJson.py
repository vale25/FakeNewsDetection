import ast
from Variables import *

Lucavar_real = real_news_json
Lucavar_fake = fake_news_json


newreal = open("/media/luca/Windows8_OS/Json_dataset_FakeReal_Twitter/dataset_twitter_finale/10NewsUser_real.json", "w")
newfake = open("/media/luca/Windows8_OS/Json_dataset_FakeReal_Twitter/dataset_twitter_finale/10NewsUser_fake.json", "w")

with open(Min10News_users,'r') as dataset:
    for line in dataset:
        article = ast.literal_eval(line)
        if article['type_page'] == "Mainstream" :
            newreal.write(line)
        else:
            newfake.write(line)

dataset.close()
newreal.close()
newfake.close()