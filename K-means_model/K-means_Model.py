from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.externals import joblib

mydata = pd.read_json("trainset_senza_duplicati.json", lines=True)
df = pd.DataFrame(mydata)

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df.text.tolist())

true_k = 2
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print

import cPickle
# save the classifier
with open('Kmeans_vectorizer.pkl', 'wb') as fid:
    cPickle.dump(vectorizer, fid)

with open('Kmeans_cluster.pkl', 'wb') as fid:
    cPickle.dump(model, fid)