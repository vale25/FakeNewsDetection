from pymongo import MongoClient
from tempfile import NamedTemporaryFile
import shutil
import csv
from csv2dict import csv_dict_list


# crea la lista di dict con le info della matrice completa
list_dict = csv_dict_list("/media/valentina/Data/tesi/userMatrix_clusterMisti/userMatrix_perDict.csv")
print list_dict

users = []
input = open("/media/valentina/Data/tesi/utenti_ordinegiusto.txt", "r")
for line in input:
    users.append(int(line))

client = MongoClient('localhost:27017')
database = client['twitter']
collection = database['tweets']


record = collection.find({ "Tweet.user.id": {"$in": users}, "Tweet.retweetedStatus.user.id": {"$exists": "true"}})
#records[elem] = record

retweets = {}
for elem in record:

    tweet = elem["Tweet"]
    user = tweet["user"]
    idUser = user["id"]
    rt = tweet["retweetedStatus"]
    us = rt["user"]
    idRetweeted = us["id"]
    if retweets.has_key(idUser):
        retweets[idUser].setdefault(idRetweeted, []).append(1)
    else:
        retweets[idUser] = {}
        retweets[idUser].setdefault(idRetweeted, []).append(1)

#print retweets

keys = retweets.keys()

# crea un dict in cui la chiave e' l'id dell'utente che ha retwittato la news, e il valore e' a sua volta un dict
# con chiave id dell'utente che e' stato retwittato e valore il numero di retweet
retweets_numbers = {}

for k in keys:
    retw = retweets[k].keys()
    for rt in retw:
        num = len(retweets[k][rt])
        if retweets_numbers.has_key(k):
            retweets_numbers[k][rt] = num
        else:
            retweets_numbers[k] = {}
            retweets_numbers[k][rt] = num

#print retweets_numbers

def updateMatrix():
    filename = '/media/valentina/Data/tesi/userMatrix_clusterMisti/userMatrix_modifica.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    # usati per creare la matrice relativa ai cluster misti real/fake
    fields = ["user_id", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10",
              "c11", "c12", "c13", "c14", "c15", "c16", "c17", "c18", "c19", "c20",
              "c21", "c22", "c23", "c24", "c25", "c26", "c27", "c28", "c29", "c30",
              "c31", "c32", "c33", "c34", "c35", "c36", "c37", "c38", "c39", "c40"]

    fields_2 = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10",
              "c11", "c12", "c13", "c14", "c15", "c16", "c17", "c18", "c19", "c20",
              "c21", "c22", "c23", "c24", "c25", "c26", "c27", "c28", "c29", "c30",
              "c31", "c32", "c33", "c34", "c35", "c36", "c37", "c38", "c39", "c40"]

    # usati per creare la matrice relativa ai cluster divisi per real e fake
    '''fields = ["user_id", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10",
              "r11", "r12", "r13", "r14", "r15", "r16", "r17", "r18", "r19", "r20",
              "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10",
              "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20"]

    fields_2 = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10",
                "r11", "r12", "r13", "r14", "r15", "r16", "r17", "r18", "r19", "r20",
                "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10",
                "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20"]'''

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            # se l'id utente appare nella lista dei retweets ovvero ha retwittato almeno un altro utente
            if retweets_numbers.has_key(int(row["user_id"])):
                # creo una lista degli utenti che l'utente in questione ha retwittato
                retweeted = retweets_numbers[int(row["user_id"])].keys()
                print "--------------------------"
                print "utente: ",row["user_id"]
                # per ognuno degli utenti retwittati
                for u in retweeted:
                    print "utente retwittato: ",u
                    if list_dict.has_key(str(u)):

                        # prendo i vari valori dei cluster

                        valori = list_dict.get(str(u))

                        # per ogni cluster
                        for elem in fields_2:

                            if int(valori.get(elem)) > 0:

                                alfa = 0.1*float(valori.get(elem))
                                print elem, "prima", row[elem]
                                # aggiorno il valore del cluster relativo all'utente che ha retwittato
                                row[elem] = float(row[elem])+alfa
                                print "alfa", alfa
                                print elem, "dopo", row[elem]
                newrow = {"user_id": row["user_id"],
                          "c1": row["c1"], "c2": row["c2"], "c3": row["c3"], "c4": row["c4"],
                          "c5": row["c5"], "c6": row["c6"], "c7": row["c7"], "c8": row["c8"], "c9": row["c9"],
                          "c10": row["c10"], "c11": row["c11"], "c12": row["c12"], "c13": row["c13"], "c14": row["c14"],
                          "c15": row["c15"], "c16": row["c16"], "c17": row["c17"], "c18": row["c18"], "c19": row["c19"],
                          "c20": row["c20"],
                          "c21": row["c21"], "c22": row["c22"], "c23": row["c23"], "c24": row["c24"],
                          "c25": row["c25"], "c26": row["c26"], "c27": row["c27"], "c28": row["c28"], "c29": row["c29"],
                          "c30": row["c30"], "c31": row["c31"], "c32": row["c32"], "c33": row["c33"], "c34": row["c34"],
                          "c35": row["c35"], "c36": row["c36"], "c37": row["c37"], "c38": row["c38"], "c39": row["c39"],
                          "c40": row["c40"]}
                writer.writerow(newrow)
            else:
                writer.writerow(row)

    shutil.move(tempfile.name, filename)


updateMatrix()