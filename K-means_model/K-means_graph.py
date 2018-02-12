from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd
from Variables import *
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib


#QUESTA CLASSE TRASFORMA I TESTI SOTTO FORMA DI STRINGHE IN UNA MATRICE DI PESI NUMERICI TRAMITE LA PESATURA TF-IDF
#PER POTERLA DARE SUCCESSIVAMENTE IN PASTO AL METODO K-MEANS STESSO. TALE METODO DETERMINA UNA DIVISIONE DELLE NOTIZIE
#IN DUE CLUSTERS (IN CUI SONO RIPORTATI I CENTROIDI ASSOCIATI) E VERIFICA GRAFICAMENTE SE E' POSSIBILE INDIVIDUARE UN
#PATTERN SULLA BASE DELLA SIMILARITA' (TF-IDF) PER CUI LE NOTIZIE FAKE RIENTRANO NEL CLUSTER FAKE E VICEVERSA.

mydata = pd.read_json(threeThousand_elements, lines=True)
df = pd.DataFrame(mydata)
train = df.text.tolist()
labels = df.label.tolist()
labels_bin=[]
for elem in labels:
    if elem == "FAKE":
        labels_bin.append(0)
    else:
        labels_bin.append(1)
print(labels_bin)

colors= ["xkcd:orange","xkcd:green"]
labels_name= ["fake","real"]

vect = TfidfVectorizer()
X = vect.fit_transform(train).todense()


pca = PCA(n_components=2).fit(X)
data2D = pca.transform(X)
a = plt.scatter(data2D[:,0], data2D[:,1], c=labels_bin, cmap=matplotlib.colors.ListedColormap(colors))
#cb = plt.colorbar()
loc = np.arange(0,max(labels_bin),max(labels_bin)/float(len(colors)))
#cb.set_ticks(loc)
#cb.set_ticklabels(labels_name)


kmeans = KMeans(n_clusters=2).fit(X)
centers2D = pca.transform(kmeans.cluster_centers_)

plt.hold(True)
plt.scatter(centers2D[:,0], centers2D[:,1],
            marker='x', s=300, linewidths=15, c='black')

plt.legend((a,a),
           ('fake', 'real'),
           scatterpoints=1,
           loc='upper right',
           bbox_to_anchor=(1.0, 1.10),
           ncol=2,
           fontsize=10)

ax = plt.gca()
leg = ax.get_legend()
leg.legendHandles[0].set_color('xkcd:orange')
leg.legendHandles[1].set_color('xkcd:green')
plt.title("K-means analysis Fake-Real news")
plt.show()
