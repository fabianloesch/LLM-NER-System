from app.llm_gateway.llm_gateway_service import LlmGatewayService
from app.db.mongo_db_client import MongoDbClient
from bson import ObjectId

class UsageService:

    def __init__(self, mongo_db_client: MongoDbClient, llm_gateway_service: LlmGatewayService = None):
        self._mongo_db_client = mongo_db_client
        self._llm_gateway = llm_gateway_service

    async def create_usage_response(self, text: str, entity_classes: list, llm_id: str):
        entities = (await self._llm_gateway.run_ner_model(text, entity_classes, llm_id))["response"]
        result = {
            "text": text,
            "entity_classes": entity_classes,
            "model": llm_id,
            "entities": entities
        }
        self._mongo_db_client.insert_one(
            self._mongo_db_client.usage_collection,
            result
        )
        return result
    
    def get_all_model_runs(self, filter: dict = None):
        projection = {"_id": 1, "model": 1, "created_datetime_utc": 1}
        result = self._mongo_db_client.get_many(
            self._mongo_db_client.usage_collection,
            filter,
            projection=projection
        )
        return result
    
    def get_model_run_by_id(self, id: str):
        result = self._mongo_db_client.get_one(
            self._mongo_db_client.usage_collection,
            {"_id": ObjectId(id)}
        )
        return result