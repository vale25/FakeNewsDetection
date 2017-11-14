from gensim.models import KeyedVectors

# Creating the model
en_model = KeyedVectors.load_word2vec_format('/media/valentina/Data/pretrained_data/GoogleNews-vectors-negative300.bin', binary=True)

# Getting the tokens
words = []
for word in en_model.vocab:
    words.append(word)

# Printing out number of tokens available
print("Number of Tokens: {}".format(len(words)))

# Printing out the dimension of a word vector
print("Dimension of a word vector: {}".format(
    len(en_model[words[0]])
))
