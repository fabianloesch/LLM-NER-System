from app.openrouter.openrouter_service import OpenRouterService
import re

class EvaluationService:

    def __init__(self, openrouter_service: OpenRouterService = None):
        self._openrouter = openrouter_service

    def create_ner_evaluation(self, text: str, entity_classes: list, llm_id: str):
        raise NotImplementedError
    