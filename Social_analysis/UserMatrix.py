import re
from pymongo import MongoClient
from collections import Counter
from User_News_Twitter import activeUsers
from datetime import datetime


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

# data di oggi
today = datetime.today()

#i = 0
with open('/media/valentina/Data/tesi/userMatrix.txt', 'w') as the_file:
    for doc in record:

        #if i < 10:
        tweet = doc['Tweet']
        user = tweet["user"]
        user_id = user['id']
        #print("userId")
        #print(user_id)

        screen_name = user['screenName']
        Screen_name = len(screen_name)
        Numbers = (re.findall(r"\d+", screen_name))
        if Numbers == []:
            NumbersElem = 0
        else:
            Numbers2 = list(Numbers[0])
            NumbersElem = len(Numbers2)


        #print ("Screen name lenght:")
        #print Screen_name
        #print ("numbers in screen Name")
        #print NumbersElem

        Username = user['name']
        User_Name_lenght = len(Username)

        #print("UserName lenght:")
        #print User_Name_lenght

        UserBio = user['description']
        User_bio_lenght = len(UserBio)

        #print("User biography lenght:")
        #print User_bio_lenght

        UserFriends = user['friendsCount']

        #print("User friendsCount:")
        #print UserFriends

        UserFollowers = user['followersCount']

        #print("User followersCount:")
        #print UserFollowers

        UserFavourites = user['favouritesCount']

        #print("User favouritesCount:")
        #print UserFavourites

        Userstatuses = user['statusesCount']

        #print("User statusesCount:")
        #print Userstatuses

        Userlisted = user['listedCount']

        #print("User listedCount:")
        #print Userlisted

        created_at = user["createdAt"]
        date = datetime.strptime(created_at, '%b %d, %Y %I:%M:%S %p')
        time = today - date
        age = time.days
        #print "account age:"
        #print age

        MediaPostScritti = Userstatuses / age
        #print("Media post:")
        #print(MediaPostScritti)

        the_file.write(str(user_id) + "," + str(Screen_name) + "," + str(NumbersElem) + "," +
                       str(User_Name_lenght) + "," + str(User_bio_lenght) + "," +
                       str(UserFriends) + "," + str(UserFollowers) + "," + str(UserFavourites) + "," +
                       str(Userstatuses) + "," + str(Userlisted) + "," + str(age) + "," +
                       str(MediaPostScritti) + "\n" )


        #i+=1