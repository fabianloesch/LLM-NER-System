from app.openrouter.openrouter_service import OpenRouterService
import re

class UsageService:

    def __init__(self, openrouter_service: OpenRouterService = None):
        self._openrouter = openrouter_service

    def run_ner_model(self, text: str, entity_classes: list, llm_name: str):
        content = self._openrouter.send_prompt(text, entity_classes, llm_name)["choices"][0]["message"]["content"]
        entities = self.inline_ner_to_json(content)
        result = {
            "text": text,
            "labels": entity_classes,
            "model": llm_name,
            "entities": entities
        }
        return result
    
    def inline_ner_to_json(self, text: str):
        pattern = re.compile(r"<(?P<label>\w+)>(?P<value>.*?)</\1>")
        
        result = []
        current_pos = 0
        last_end = 0

        for match in pattern.finditer(text):
            # Text vor der Entität
            before = text[last_end:match.start()]
            current_pos += len(before)

            value = match.group("value")
            label = match.group("label")

            start = current_pos
            end = start + len(value)

            result.append({"start":start, "end":end, "label":label, "entity": value})

            current_pos = end
            last_end = match.end()

        return result