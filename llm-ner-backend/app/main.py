from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import usage_router, available_models_router, evaluation_router

app = FastAPI()

# CORS Middleware konfigurieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:5173",  # Vue.js Dev-Server
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Erlaubt alle HTTP-Methoden (GET, POST, etc.)
    allow_headers=["*"],  # Erlaubt alle Headers
)

app.include_router(available_models_router.router, prefix="/api", tags=["Model Information"] )
app.include_router(usage_router.router, prefix="/api", tags=["Model Run"] )
app.include_router(evaluation_router.router, prefix="/api", tags=["Model Evaluation"] )

# cd llm-ner-backend
# C:\Users\loesc\Documents\Studium_Dokumente\FU_Hagen\Module\CIE\LLM-NER-System\llm-ner-backend\env\Scripts\activate.bat
# uvicorn app.main:app --reload

# pip install -r requirements.txt