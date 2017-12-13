import ast

Lucavar_real = "/home/luca/PycharmProjects/TagMe_analisys_JsonVersion/real.json"
Lucavar_fake = "/home/luca/PycharmProjects/TagMe_analisys_JsonVersion/fake.json"


newreal = open(Lucavar_real, "w")
newfake = open(Lucavar_fake, "w")

with open("/home/luca/PycharmProjects/FakeNewsDetection/K-means_model/trainset_senza_duplicati.json",'r') as dataset:
    for line in dataset:
        article = ast.literal_eval(line)
        if article['label'] == "REAL" :
            newreal.write(line)
        else:
            newfake.write(line)

dataset.close()
newreal.close()
newfake.close()