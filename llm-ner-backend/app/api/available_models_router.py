from fastapi import APIRouter, Depends
from app.models.available_models_dtos import AvailableModelsResponseDto
from app.openrouter.openrouter_service import OpenRouterService
from app.openrouter.openrouter_client import OpenRouterClient
from app.services.usage_service import UsageService

router = APIRouter()

def get_openrouter_service():
    return OpenRouterService(OpenRouterClient())

@router.get("/availableModels", response_model=AvailableModelsResponseDto)
def create_new_model_run(
    openrouter_service: OpenRouterService = Depends(get_openrouter_service)
):
    result = openrouter_service.get_available_models()
    return {"result": result}