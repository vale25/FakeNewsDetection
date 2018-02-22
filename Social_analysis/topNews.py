from pymongo import MongoClient
import pprint

client = MongoClient('localhost:27017')

database = client['twitter']
collection = database['tweets']

record = collection.find()

retweets = {}
favorites = {}

for elem in record:
    tweet = elem["Tweet"]
    rt = tweet["retweetCount"]
    url = elem["url_tweet"]
    type = elem["type_page"]
    retweets[url] = [rt, type]
    if "retweetedStatus" in tweet:
        rtStatus = tweet["retweetedStatus"]
        fav_interno = rtStatus["favoriteCount"]
        favorites[url] = [fav_interno, type]

retweets_10 = sorted(retweets.items(), key=lambda x: x[1], reverse=True)[:10]
favorites_10 = sorted(favorites.items(), key=lambda x: x[1], reverse=True)[:10]

file = open("/media/valentina/Data/tesi/popularNews.txt", "w")

print "prime dieci news con piu' retweet in Tweet"
file.write("prime dieci news con piu' retweet\n")
for x in retweets_10:
    file.write(str(x[1])+" "+x[0]+"\n")
    print x[1], x[0]

print "-------------"
print "prime dieci news con piu' like in Tweet"
file.write("prime dieci news con piu' like\n")
for x in favorites_10:
    file.write(str(x[1]) + " " + x[0]+"\n")
    print x[1], x[0]