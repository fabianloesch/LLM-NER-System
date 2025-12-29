from fastapi import FastAPI
from app.api import usage_router, available_models_router, evaluation_router

app = FastAPI()
app.include_router(available_models_router.router, prefix="/api", tags=["Model Information"] )
app.include_router(usage_router.router, prefix="/api", tags=["Model Run"] )
app.include_router(evaluation_router.router, prefix="/api", tags=["Model Evaluation"] )

# cd llm-ner-backend
# C:\Users\loesc\Documents\Studium_Dokumente\FU_Hagen\Module\CIE\LLM-NER-System\llm-ner-backend\env\Scripts\activate.bat
# uvicorn app.main:app --reload

# pip install -r requirements.txt