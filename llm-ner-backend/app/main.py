from fastapi import FastAPI
from app.api import usage_router, available_models_router, evaluation_router

app = FastAPI()
app.include_router(available_models_router.router, prefix="/api", tags=["Model Information"] )
app.include_router(usage_router.router, prefix="/api", tags=["Model Run"] )
app.include_router(evaluation_router.router, prefix="/api", tags=["Model Evaluation"] )