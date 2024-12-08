import pymongo
from src import configs
import json
from bson import json_util

def select_all_from_mongodb(collection_name: str):

    conn = configs.get_connection()
    db = conn[configs.news_db]

    collection = db[collection_name]

    docs = collection.find({})

    return json.loads(json_util.dumps(docs))

