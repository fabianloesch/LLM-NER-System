from app.openrouter.openrouter_service import OpenRouterService
from app.models.evaluation_dtos import CorpusEntry
import app.core.utils as utils
from app.db.mongo_db_client import MongoDbClient
from bson import ObjectId

class EvaluationService:

    def __init__(self, mongo_db_client: MongoDbClient, openrouter_service: OpenRouterService = None):
        self._mongo_db_client = mongo_db_client
        self._openrouter = openrouter_service

    async def create_evaluation_response(self, corpus: list[CorpusEntry], llm_ids: list[str]):
        entity_classes = utils.get_distinct_entity_classes(corpus)
        batch_run = await self._openrouter.run_ner_model_batch(corpus, entity_classes, llm_ids)
        result = {}
        for llm_id in llm_ids:
            llm_base_metrics = {}
            for entry in corpus:
                pred = batch_run[llm_id][entry["id"]]
                entry_base_metrics = utils.compute_base_eval_metric(truth=entry, prediction=pred)
                llm_base_metrics = utils.add_base_metrics_dicts(llm_base_metrics, entry_base_metrics)
            llm_eval_result = utils.compute_eval_metrics(llm_base_metrics)
            result[llm_id] = llm_eval_result
        result = {
            "models": llm_ids,
            "entity_classes": entity_classes,
            "evaluations": result
            }
        self._mongo_db_client.insert_one(
            self._mongo_db_client.evaluation_collection,
            result
        )
        return result
    
    def get_all_model_evaluations(self, filter: dict = None):
        projection = {"_id": 1, "models": 1, "created_datetime_utc": 1}
        result = self._mongo_db_client.get_many(
            self._mongo_db_client.evaluation_collection,
            filter,
            projection=projection
        )
        return result
    
    def get_model_evaluation_by_id(self, id: str):
        result = self._mongo_db_client.get_one(
            self._mongo_db_client.evaluation_collection,
            {"_id": ObjectId(id)}
        )
        return result