from app.openrouter.openrouter_client import OpenRouterClient
from datetime import datetime, timezone
import app.core.utils as utils

class OpenRouterService:
    def __init__(self, client: OpenRouterClient):
        self.client = client

    def get_available_models(self):
        models_detailed = self.client.get_available_models()["data"]
        models_compact = [
            {
                "id": m["id"],
                "name": m["name"],
                "createdAtUtc": datetime.fromtimestamp(m["created"], tz=timezone.utc)
            }
            for m in models_detailed
        ]
        return models_compact
 
    def run_ner_model(self, text: str, entity_classes: list, llm_id: str) -> str:
        prompt = f"""
            Ich möchte dich als Named-Entity-Recognition-Modell für medizinische Texte benutzen. Deine Aufgabe ist es in Texten bestimmte Entitäten zu erkennen.  
            Um Teile des Textes als Entität zu kennzeichen, nutze bitte eine Inline-Maskierung nach dem Format <entityClassName>exampleEntity</entityClassName>. 
            Gebe bitte immer den gesamten Eingabetext inklusive der Maskierung als Antwort wieder. 
            Beispiel: Bei der Entitätsklasse "Indication" und dem Text "Der Arzt verschreibt Amoxicillin wegen bakterieller Bronchitis." müsste die Antwort folgendermaßen lauten: "Der Arzt verschreibt Amoxicillin wegen <Indication>bakterieller Bronchitis</Indication>.".
            Neben den Entitätsmaskierungen darfst du auf keinen Fall weitere Zeichen zum Text hinzufügen.
            Es ist sehr wichtig, dass die Antwort diesem Format entspricht, da sie sonst nicht verwendet werden kann. Antworte nur mit diesem Format, ohne weiteren Text, Erklärungen oder sonstige vorgestellte Zeichen.
            Möglicherweise sind in dem zu untersuchenden Text keine Entitäten der relevanten Entitätsklassen zu finden. Sollte dies der Fall sein, gib bitte exakt den Eingabetext ohne Entitätsmaskierungen wieder. 
            Es werden nur Entitäten folgender Entitätsklassen gesucht: {", ".join(entity_classes)}.
            Hier ist der Text:
            {text}
            """

        response = self.client.create_chat_completition(prompt, llm_id)["choices"][0]["message"]["content"]
        response = utils.inline_ner_to_json(response)

        # OpenRouter Response extrahieren
        return response