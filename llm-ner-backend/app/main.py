from fastapi import FastAPI
from app.api import usage_router

app = FastAPI()
app.include_router(usage_router.router, prefix="/api")