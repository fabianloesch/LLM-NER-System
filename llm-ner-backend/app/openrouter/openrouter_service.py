from app.openrouter.openrouter_client import OpenRouterClient
from datetime import datetime, timezone

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
 
    def run_ner_model(self, text: str, entityclasses: list, llm_id: str) -> str:
        prompt = f"""
            Ich möchte dich als Named-Entity-Recognition-Modell für medizinische Texte benutzen. Deine Aufgabe ist es in Texten bestimmte Entitäten zu erkennen. 
            Es werden Entitäten folgender Entitätsklassen gesucht: {", ".join(entityclasses)}. 
            Um Teile des Textes als Entität zu kennzeichen, nutze bitte eine Inline-Maskierung nach dem Format <entityClassName>exampleEntity</entityClassName>. 
            Gebe bitte immer den gesamten Eingabetext inklusive der Maskierung als Antwort wieder. 
            Beispiel: Bei der Entitätsklasse "Drug" und dem Text "Der Arzt gibt dem Patienten Ibuprofen." müsste die Antwort folgendermaßen lauten: "Der Arzt gibt dem Patienten <Drug>Ibuprofen</Drug>.".
            Neben den Entitätsmaskierungen darfst du auf keinen Fall weitere Zeichen zum Text hinzufügen.
            Es ist sehr wichtig, dass die Antwort diesem Format entspricht, da sie sonst nicht verwendet werden kann. Antworte nur mit diesem Format, ohne weiteren Text, Erklärungen oder sonstige vorgestellte Zeichen.
            Möglicherweise sind in dem zu untersuchenden Text keine Entitäten der relevanten Entitätsklassen zu finden. Sollte dies der Fall sein, gib bitte exakt den Eingabetext ohne Entitätsmaskierungen wieder. 
            Hier ist der Text:
            {text}
            """

        response = self.client.create_chat_completition(prompt, llm_id)

        # OpenRouter Response extrahieren
        return response