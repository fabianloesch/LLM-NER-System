from app.openrouter.openrouter_service import OpenRouterService

class UsageService:

    def __init__(self, openrouter_service: OpenRouterService = None):
        self._openrouter = openrouter_service

    async def create_usage_response(self, text: str, entity_classes: list, llm_id: str):
        entities = (await self._openrouter.run_ner_model(text, entity_classes, llm_id))["response"]
        result = {
            "text": text,
            "labels": entity_classes,
            "model": llm_id,
            "entities": entities
        }
        return result