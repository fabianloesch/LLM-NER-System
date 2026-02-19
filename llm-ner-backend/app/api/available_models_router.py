from fastapi import APIRouter, Depends
from app.models.available_models_dtos import AvailableModelsResponseDto
from app.llm_gateway.llm_gateway_service import LlmGatewayService
from app.llm_gateway.llm_gateway_client import LlmGatewayClient

router = APIRouter()

def get_llm_gateway_service():
    return LlmGatewayService(LlmGatewayClient())

@router.get("/availableModels", response_model=AvailableModelsResponseDto)
async def get_available_models(
    llm_gateway_service: LlmGatewayService = Depends(get_llm_gateway_service)
):
    result = await llm_gateway_service.get_available_models()
    return {"result": result}