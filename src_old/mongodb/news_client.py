from ..configs import get_settings
from pymongo import MongoClient

class NewsClient:

    def __init__(
        self, db_name: str = "news", collection_name: str = "hespress"
    ):
        super(NewsClient, self).__init__()
        
        settings = get_settings()
        MONGO_URL = f"mongodb://{settings.user_name}:{settings.password}@{settings.host}:{settings.port}/"

        try: 
            self._client = MongoClient(MONGO_URL)
            self.db = self._client[db_name]
            self.collection = self.db[collection_name]
        except Exception as e: 
            raise ConnectionError("cannot connect to mongo database.")
        
    def listdbs(self):
        return self._client.list_database_names()
    
    def find(self, filter: dict = {}):
        return self.collection.find(filter)

    def insert(self, news: dict):
        self.collection.insert_one(news) 

    def insert_many(self, news_list: list[dict]):
        self.collection.insert_many(news_list) 

    def clear(self):
        self.collection.delete_many({})
        