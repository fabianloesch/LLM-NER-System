import requests
from app.core.config import config

class OpenRouterClient:
    BASE_URL = config.OPENROUTER_URL

    def __init__(self):
        self.headers = {
            "Authorization": config.OPENROUTER_API_KEY,
            "Content-Type": "application/json",
        }

    def create_response(self, prompt: str, model: str) -> dict:
        payload = {
            "model": model,
            "messages": [
                {
                    "role": Roles.user,
                    "content": prompt
                }
            ],
        }

        response = requests.post(
            self.BASE_URL,
            json=payload,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()
    

class Roles:
    system = "system"
    user = "user"
    assistant = "assistant"