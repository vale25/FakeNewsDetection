import gensim, logging, os, zipfile, numpy as np
from keras.layers import Embedding, merge
from keras.engine import Input, Model

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

sentences = MySentences('/home/valentina/Documenti/tesi/testi')



#sentences = [['first', 'sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
model = gensim.models.Word2Vec(sentences)
# get the word vector of "the"
#print(model.wv['first'])

# stampa le 3 parole piu' comuni
print("parole piu' comuni")
print(model.wv.index2word[0], model.wv.index2word[1], model.wv.index2word[2])

# get the least common words
print("parole meno comuni")
vocab_size = len(model.wv.vocab)
print(model.wv.index2word[vocab_size - 1], model.wv.index2word[vocab_size - 2], model.wv.index2word[vocab_size - 3])

# stampa l'intero vocabolario
i = 0
while i<vocab_size:
    print(model.wv.index2word[i])
    i+=1

# some similarity fun - usa la coseno similarita'
print(model.wv .similarity('sun', 'universe'), model.wv.similarity('sun', 'book'))

# stampa la parola meno simile alle altre
print(model.wv.doesnt_match("atlantic universe europe".split()))
print(model.wv.doesnt_match("atlantic china book europe".split()))

# convert the input data into a list of integer indexes aligning with the wv indexes
# Read the data into a list of strings.
def read_data(filename):
    """Extract the first file enclosed in a zip file as a list of words."""
    with zipfile.ZipFile(filename) as f:
        data = f.read(f.namelist()[0]).split()
    return data

def convert_data_to_index(string_data, wv):
    index_data = []
    for word in string_data:
        if word in wv:
            index_data.append(wv.vocab[word].index)
    return index_data

str_data = read_data('/home/valentina/Documenti/tesi/testi/cosmos.zip')
index_data = convert_data_to_index(str_data, model.wv)
print(str_data[:4], index_data[:4])

# save and reload the model
#model.save(root_path + "mymodel")
#model = gensim.models.Word2Vec.load(root_path + "mymodel")

# convert the wv word vectors into a numpy matrix that is suitable for insertion
# into our TensorFlow and Keras models
embedding_matrix = np.zeros((len(model.wv.vocab), 100))
for i in range(len(model.wv.vocab)):
    embedding_vector = model.wv[model.wv.index2word[i]]
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector


valid_size = 5  # Random set of words to evaluate similarity on.
valid_window = 100  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)
# input words - in this case we do sample by sample evaluations of the similarity
valid_word = Input((1,), dtype='int32')
other_word = Input((1,), dtype='int32')
# setup the embedding layer
embeddings = Embedding(input_dim=embedding_matrix.shape[0], output_dim=embedding_matrix.shape[1],
                      weights=[embedding_matrix])
embedded_a = embeddings(valid_word)
embedded_b = embeddings(other_word)
similarity = merge([embedded_a, embedded_b], mode='cos', dot_axes=2)
# create the Keras model
k_model = Model(input=[valid_word, other_word], output=similarity)

def get_sim(valid_word_idx, vocab_size):
    sim = np.zeros((vocab_size,))
    in_arr1 = np.zeros((1,))
    in_arr2 = np.zeros((1,))
    in_arr1[0,] = valid_word_idx
    for i in range(vocab_size):
        in_arr2[0,] = i
        out = k_model.predict_on_batch([in_arr1, in_arr2])
        sim[i] = out
    return sim

# now run the model and get the closest words to the valid examples
for i in range(valid_size):
    valid_word = model.wv.index2word[valid_examples[i]]
    top_k = 8  # number of nearest neighbors
    sim = get_sim(valid_examples[i], len(model.wv.vocab))
    nearest = (-sim).argsort()[1:top_k + 1]
    log_str = 'Nearest to %s:' % valid_word
    for k in range(top_k):
        close_word = model.wv.index2word[nearest[k]]
        log_str = '%s %s,' % (log_str, close_word)
    print(log_str)