import pymongo

user = "luca04"
password = "pinguepinga1"

client = pymongo.MongoClient("mongodb://%s:%s@ds111876.mlab.com:11876/politicsnewsdb" %(user, password))

db = client.politicsnewsdb

result = db.politicsnewsdb.insert_one(
    {
        "_id": "2",
        "topic": "White House 'has plan to replace Tillerson'",
        "text" : "",
        "link" : "http://www.bbc.com/news/world-us-canada-42187070"
    }
)

# print the number of documents in a collection
print db.cool_collection.count()

