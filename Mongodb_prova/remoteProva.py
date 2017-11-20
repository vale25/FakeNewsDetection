import pymongo

user = ""
password = ""

client = pymongo.MongoClient("mongodb://%s:%s@ds111876.mlab.com:11876/politicsnewsdb" %(user,password))

db = client.politicsnewsdb

result = db.politicsnewsdb.insert_one(
    {
        "_id": "4",
        "text" : "you have a very fat ass"
    }
)

# print the number of documents in a collection
print db.cool_collection.count()

