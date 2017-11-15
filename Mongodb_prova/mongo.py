from pymongo import MongoClient

client = MongoClient()
db = client.webnews


result = db.webnews.insert_one(
    {
        "text" : "Donald Trump is a man "
    }
)
