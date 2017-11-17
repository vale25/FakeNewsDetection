import pymongo

client = pymongo.MongoClient("mongodb://luca04:pinguepinga1@ds111876.mlab.com:11876/politicsnewsdb")

db = client.politicsnewsdb

result = db.politicsnews.insert_one(
    {
        "_id": "3",
        "text" : "Donald Trump won the elections"
    }
)

# print the number of documents in a collection
print db.politicsnews.count()

