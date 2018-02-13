import re
from pymongo import MongoClient
from collections import Counter

def activeUsers():

    client = MongoClient('localhost:27017')

    database = client['twitter']
    collection = database['tweets']
    record = collection.find()
    #print(record)

    #Conta il numero di id utente nel dataset tweets
    Users = collection.find({"Tweet.user.id": {"$exists": True}}).count()
    #print(Users)

    #Crea la lista di utenti twitter ed appendi gli id degli utenti nel dataset Tweets
    users = []
    for doc in record:
        tweet = doc['Tweet']
        user = tweet["user"]
        user_id= user['id']
        users.append(user_id)



    #Conta le volte che ogni id utente appare nella lista
    User_id_countDuplicates = Counter(users)
    #print(User_id_countDuplicates)

    #Trova gli utenti che hanno letto almeno 10 news
    Final_dict = {k:v for (k,v) in User_id_countDuplicates.items() if v > 9}
    #print(Final_dict)
    #Tot_Users = len(Final_dict)
    #print("Users totali:")
    #print(Tot_Users)

    return Final_dict

#GLI UTENTI CHE HANNO LETTO ALMENO DIECI NEWS SONO IN TOTALE 1159

#Features da prendere: followersCount,friendsCount,favouritesCount,statusesCount,notizie lette/pubblicate