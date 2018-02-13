import re
from pymongo import MongoClient
from collections import Counter
from User_News_Twitter import activeUsers

client = MongoClient('localhost:27017')

database = client['twitter']
collection = database['tweets']

record = collection.find()

# prendo gli id degli utenti che hanno letto almeno 10 news
users_id = activeUsers().keys()
#print users_id

news = collection.aggregate([{"$group": { "_id": "$Tweet.user.id", "id_news": { "$addToSet": "$_id"} } }])


id_news = []
for doc in news:
    id_utente = doc["_id"]
    if id_utente in users_id:
        id_notizia = doc["id_news"][0]
        id_news.append(id_notizia)

record = collection.find({"_id": {"$in":id_news} })
print record.count()

i = 0
with open('Prova.txt', 'w') as the_file:
    for doc in record:

        if i < 2:
            tweet = doc['Tweet']
            user = tweet["user"]
            user_id = user['id']
            print("userId")
            print(user_id)

            screen_name = user['screenName']
            Screen_name = len(screen_name)
            Numbers = (re.findall(r"\d+", screen_name))
            if Numbers == []:
                NumbersElem = 0
            else:
                Numbers2 = list(Numbers[0])
                NumbersElem = len(Numbers2)


            print ("Screen name lenght:")
            print Screen_name
            print ("numbers in screen Name")
            print NumbersElem

            Username = user['name']
            User_Name_lenght = len(Username)

            print("UserName lenght:")
            print User_Name_lenght

            UserBio = user['description']
            User_bio_lenght = len(UserBio)

            print("User biography lenght:")
            print User_bio_lenght

            UserFriends = user['friendsCount']

            print("User friendsCount:")
            print UserFriends

            UserFollowers = user['followersCount']

            print("User followersCount:")
            print UserFollowers

            UserFavourites = user['favouritesCount']

            print("User favouritesCount:")
            print UserFavourites

            Userstatuses = user['statusesCount']

            print("User statusesCount:")
            print Userstatuses

            Userlisted = user['listedCount']

            print("User listedCount:")
            print Userlisted

            '''MediaPostScritti = Userstatuses / age
            print("Media post:")
            print(MediaPostScritti)'''

            the_file.write(str(user_id) + "," + str(Screen_name) + "," + str(NumbersElem) + "," + str(User_Name_lenght) + "," + str(User_bio_lenght) + "," + str(UserFriends) + "," + str(UserFollowers) + "," + str(UserFavourites) + "," + str(Userstatuses) + "," + str(Userlisted) + "\n" )


        i+=1

''''#Query per prendere gli id
user_id = collection.find( {},  {"Tweet.user.id":1, "_id":0}).limit(100)

#Query per prendere gli screenName
screenName = collection.find( {},  {"Tweet.user.screenName":1, "_id":0}).limit(100)

#Query per prendere gli user_name
UserName = collection.find( {},  {"Tweet.user.name":1, "_id":0}).limit(100)

#Query per prendere la bio degli users
UserBio = collection.find( {},  {"Tweet.user.description":1, "_id":0}).limit(100)

#Query per prendere contare gli amici l'utente segue
UserFriendsCount = collection.find( {},  {"Tweet.user.friendsCount":1, "_id":0}).limit(100)

#Query per prendere contare gli amici che seguono l'utente
UserFollowersCount = collection.find( {},  {"Tweet.user.followersCount":1, "_id":0}).limit(100)

#Query per prendere contare i cuori messi dall'utente
UserFavouritesCount = collection.find( {},  {"Tweet.user.favouritesCount":1, "_id":0}).limit(100)


#Query per prendere il numero di tweets dell'utente
UserStatusesCount = collection.find( {},  {"Tweet.user.statusesCount":1, "_id":0}).limit(100)


#Query per prendere il listedCount dell'utente
UserListedCount = collection.find( {},  {"Tweet.user.listedCount":1, "_id":0}).limit(100)


#Query per prendere il numero di menzioni di altri utenti per ogni utente
UserMentionCount = collection.find( {},  {"Tweet.userMentionEntities":1, "_id":0}).limit(100)


#Query per prendere il numero di hashtag per ogni utente
UserHashtagCount = collection.find( {},  {"Tweet.hashtagEntities":1, "_id":0}).limit(100)


#Query per prendere il numero di media per ogni utente
UserMediaCount = collection.find( {},  {"Tweet.mediaEntities":1, "_id":0}).limit(100)



#Crea la lista di utenti twitter ed appendi gli id degli utenti nel dataset Tweets
users_id = []
for doc in user_id:
    tweet = doc['Tweet']
    user = tweet["user"]
    user_id = user['id']
    users_id.append(user_id)

print("user_id")
print(users_id)

Screen_name = []
Numbers = []
NumbersInScreenName = []

for doc in screenName:
    tweet = doc['Tweet']
    user = tweet["user"]
    screen_name = user['screenName']
    Screen_name.append(len(screen_name))
    Numbers.append(re.findall(r"\d+", screen_name))

for elem in Numbers:
    if elem == []:
        NumbersInScreenName.append(0)
    for elem2 in elem:
        NumbersInScreenName.append(len(elem2))

print ("Screen name lenght:")
print Screen_name
print ("numbers in screen Name")
print NumbersInScreenName

User_Name_lenght = []

for doc in UserName:
    tweet = doc['Tweet']
    user = tweet["user"]
    Username = user['name']
    User_Name_lenght.append(len(Username))

print("User name lenght:")
print User_Name_lenght

User_bio_lenght = []



for doc in UserBio:
    tweet = doc['Tweet']
    user = tweet["user"]
    UserBio = user['description']
    User_bio_lenght.append(len(UserBio))

print("User biography lenght:")
print User_bio_lenght


User_friendsCount = []

for doc in UserFriendsCount:
    tweet = doc['Tweet']
    user = tweet["user"]
    UserFriends = user['friendsCount']
    User_friendsCount.append(UserFriends)

print("User friendsCount:")
print User_friendsCount



User_followersCount = []

for doc in UserFollowersCount:
    tweet = doc['Tweet']
    user = tweet["user"]
    UserFollowers = user['followersCount']
    User_followersCount.append(UserFollowers)

print("User followersCount:")
print User_followersCount



User_favouritesCount = []

for doc in UserFavouritesCount:
    tweet = doc['Tweet']
    user = tweet["user"]
    UserFavourites = user['favouritesCount']
    User_favouritesCount.append(UserFavourites)

print("User favouritesCount:")
print User_favouritesCount



User_statusesCount = []

for doc in UserStatusesCount:
    tweet = doc['Tweet']
    user = tweet["user"]
    Userstatuses = user['statusesCount']
    User_statusesCount.append(Userstatuses)

print("User statusesCount:")
print User_statusesCount



User_listedCount = []

for doc in UserListedCount:
    tweet = doc['Tweet']
    user = tweet["user"]
    Userlisted = user['listedCount']
    User_listedCount.append(Userlisted)

print("User listedCount:")
print User_listedCount



User_mentionCount = []

for doc in UserMentionCount:
    tweet = doc['Tweet']
    mention = tweet['userMentionEntities']
    User_mentionCount.append(len(mention))

print("User mentionCount:")
print User_mentionCount



User_hashtagCount = []

for doc in UserHashtagCount:
    tweet = doc['Tweet']
    hashtag = tweet['hashtagEntities']
    User_hashtagCount.append(len(hashtag))

print("User hashtagCount:")
print User_hashtagCount



User_mediaCount = []

for doc in UserMediaCount:
    tweet = doc['Tweet']
    media = tweet['mediaEntities']
    User_mediaCount.append(len(media))

print("User mediaCount:")'''
#print User_mediaCount
