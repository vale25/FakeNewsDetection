import pymongo

client = pymongo.MongoClient("mongodb://luca04:pinguepinga1@ds111876.mlab.com:11876/politicsnewsdb")

db = client.politicsnewsdb

result = db.politicsnewsdb.insert_one(
    {
        "_id": "1",
        "text" : "Donald Trump is won the elections"
    }
)

# print the number of documents in a collection
print db.cool_collection.count()

