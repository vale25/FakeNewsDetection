import gensim, logging, os


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

sentences = ('/home/valentina/Documenti/tesi/testi/oceano.txt')



#sentences = [['first', 'sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
model = gensim.models.Word2Vec(sentences)
# get the word vector of "the"
#print(model.wv['first'])

# stampa le 3 parole piu' comuni
print(model.wv.index2word[0], model.wv.index2word[1], model.wv.index2word[2])

# some similarity fun - usa la coseno similarita'
#print(model.wv.similarity('first', 'second'), model.wv.similarity('first', 'sentence'))