from app.core.config import config
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime, timezone

class MongoDbClient:
    connection_string = config.MONGO_DB_CONNECTION_STRING

    def __init__(self):
        self.client = MongoClient(self.connection_string)
        self.database =  self.client.LLM_NER_SYSTEM_DB
        self.usage_collection = self.database.Usages
        self.evaluation_collection = self.database.Evaluations

    def insert_one(self, collection: Collection, document):
        document["created_datetime_utc"] = datetime.now(timezone.utc).isoformat()
        collection.insert_one(document).inserted_id
        document["_id"] = str(document['_id'])
        return document
    
    def get_one(self, collection: Collection, filter_dict: dict):
        document = collection.find_one(filter_dict)
        if document:
            document["_id"] = str(document["_id"])
        return document
    
    def get_many(self, collection: Collection, filter_dict: dict = None, projection: dict = None):
        if filter_dict is None:
            filter_dict = {}
        documents = list(collection.find(filter_dict, projection))
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        return documents