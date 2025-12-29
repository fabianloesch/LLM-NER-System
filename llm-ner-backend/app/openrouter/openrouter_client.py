from app.core.config import config
import httpx

class OpenRouterClient:
    CHAT_COMPLETION_URL = "https://openrouter.ai/api/v1/chat/completions"
    AVAILABLE_MODELS_URL = "https://openrouter.ai/api/v1/models"

    def __init__(self):
        self.headers = {
            "Authorization": config.OPENROUTER_API_KEY,
            "Content-Type": "application/json",
        }
        self.client = httpx.AsyncClient(timeout=100.0)

    async def get_available_models(self) -> dict:
        response = await self.client.get(
            self.AVAILABLE_MODELS_URL, 
            headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def create_chat_completition(self, prompt: str, model: str) -> dict:
        payload = {
            "model": model,
            "messages": [
                {
                    "role": Roles.user,
                    "content": prompt
                }
            ],
        }

        response = await self.client.post(
            self.CHAT_COMPLETION_URL,
            json=payload,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()
    


class Roles:
    system = "system"
    user = "user"
    assistant = "assistant"