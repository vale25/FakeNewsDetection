from pymongo import MongoClient

client = MongoClient()
db = client.webnews

#result = db.webnews.delete_many({})


result = db.webnews.insert_one(
    {
        "_id": "1",
        "text" : "Donald Trump is won the elections"
    }
)
