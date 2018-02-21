from Variables import *
import numpy as np
import numpy
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler


#Print delle features con i valori di correlazione con la label
def printFeatures(correlations):
    print("correlation of screen_name_length with label real/fake:")
    print correlations[0]
    print("correlation of digits_screen_name with label real/fake:")
    print correlations[1]
    print("correlation of user_name_length with label real/fake:")
    print correlations[2]
    print("correlation of bio_length with label real/fake:")
    print correlations[3]
    print("correlation of friends with label real/fake:")
    print correlations[4]
    print("correlation of followers with label real/fake:")
    print correlations[5]
    print("correlation of favorites with label real/fake:")
    print correlations[6]
    print("correlation of statuses with label real/fake:")
    print correlations[7]
    print("correlation of user_listed with label real/fake:")
    print correlations[8]
    print("correlation of account_age with label real/fake:")
    print correlations[9]
    print("correlation of statuses/day with label real/fake:")
    print correlations[10]
    print("correlation of sentiment_score with label real/fake:")
    print correlations[11]

# load dataset
with open(UserFeatures_matrix) as f:
    lines = (line for line in f if not line.startswith('#'))
    dataset = np.loadtxt(lines, delimiter=',', skiprows=1)


X = dataset[:,1:13]
Y = dataset[:,53]

#-------------------STANDARD SCALER---------------------
#scaler = preprocessing.StandardScaler().fit(X)
#StandardScaler(copy=True, with_mean=True, with_std=True)
#X_scale = scaler.transform(X)


#-------------------QUANTILE TRANSFORMER----------------
quantile_transformer = preprocessing.QuantileTransformer(random_state=0)
X_scale = quantile_transformer.fit_transform(X)



correlation_lists = []
corr = []
correlation2 = []

for i in range(12):
    for j in range(len(X_scale)):
        corr.append(X_scale[j][i])
    correlation_lists.append(corr)
    corr = []

for i in range(12):
    correlation2.append(numpy.corrcoef(correlation_lists[i], Y)[0, 1])

printFeatures(correlation2)

correlations = []
cont = 1
for i in range(12):
    X = dataset[:,cont]
    Y = dataset[:,53]
    X = np.array(X).reshape((1, -len(X)))
    print(X.tolist())

    #--------------------NORMALIZATION--------------------
    #X_scale = preprocessing.normalize(correlations2)

    #--------------------SCALE----------------------------
    #X_scale = preprocessing.scale(X)


    #flat_list = [item for sublist in X_scale for item in sublist]
    #print(flat_list)
    #print("-------------------")
    cont+=1
    correlations2 = []

    correlations.append(numpy.corrcoef(X_scale, Y)[0, 1])




