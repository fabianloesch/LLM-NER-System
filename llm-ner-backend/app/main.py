from fastapi import FastAPI
from app.api import usage_router, available_models_router

app = FastAPI()
app.include_router(usage_router.router, prefix="/api")
app.include_router(available_models_router.router, prefix="/api")