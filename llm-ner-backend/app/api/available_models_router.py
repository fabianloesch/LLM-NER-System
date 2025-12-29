from fastapi import APIRouter, Depends
from app.models.available_models_dtos import AvailableModelsResponseDto
from app.openrouter.openrouter_service import OpenRouterService
from app.openrouter.openrouter_client import OpenRouterClient

router = APIRouter()

def get_openrouter_service():
    return OpenRouterService(OpenRouterClient())

@router.get("/availableModels", response_model=AvailableModelsResponseDto)
async def get_available_models(
    openrouter_service: OpenRouterService = Depends(get_openrouter_service)
):
    result = await openrouter_service.get_available_models()
    return {"result": result}