from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    OPENROUTER_API_KEY: str = ""
    APP_NAME: str = "LLM-NER-Backend"
    DEBUG: bool = False
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    MONGO_DB_CONNECTION_STRING: str = ""


    class Config:
        env_file = ".env"

config = Config()