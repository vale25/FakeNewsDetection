from Variables import *
import numpy as np
import numpy


# load dataset
with open(UserFeatures_matrix) as f:
    lines = (line for line in f if not line.startswith('#'))
    dataset = np.loadtxt(lines, delimiter=',', skiprows=1)

correlations = []
for i in range(12):
    X = dataset[:,i]
    Y = dataset[:,53]

    correlations.append(numpy.corrcoef(X, Y)[0, 1])

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



