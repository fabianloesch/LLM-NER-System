from app.openrouter.openrouter_service import OpenRouterService
from app.models.evaluation_dtos import CorpusEntry
import app.core.utils as utils

class EvaluationService:

    def __init__(self, openrouter_service: OpenRouterService = None):
        self._openrouter = openrouter_service

    async def create_evaluation_response(self, corpus: list[CorpusEntry], llm_ids: list[str]):
        entity_classes = utils.get_distinct_entity_classes(corpus)
        batch_run = await self._openrouter.run_ner_model_batch(corpus, entity_classes, llm_ids)
        response = {}
        for llm_id in llm_ids:
            llm_base_metrics = {}
            for entry in corpus:
                pred = batch_run[llm_id][entry["id"]]
                entry_base_metrics = utils.compute_base_eval_metric(truth=entry, prediction=pred)
                llm_base_metrics = utils.add_base_metrics_dicts(llm_base_metrics, entry_base_metrics)
            llm_eval_result = utils.compute_eval_metrics(llm_base_metrics)
            response[llm_id] = llm_eval_result
        return response