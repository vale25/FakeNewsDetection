with open('/home/luca/PycharmProjects/FakeNewsDetection/Semantic_and_sintactic_analysis/stringaDaEliminareSpazi.txt') as f:
    atext = f.read().replace('\n', ' ').replace('"', '')

print (atext)

with open("OutputStringaSenzaSpazi.txt", "w") as text_file:
    text_file.write("%s" % atext)