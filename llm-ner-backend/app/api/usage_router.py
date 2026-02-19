from fastapi import APIRouter, Depends
from app.models.usage_dtos import UsageResponseDto, UsageRequestDto, AllUsagesResponseDto
from app.llm_gateway.llm_gateway_service import LlmGatewayService
from app.llm_gateway.llm_gateway_client import LlmGatewayClient
from app.services.usage_service import UsageService
from app.db.mongo_db_client import MongoDbClient

router = APIRouter()

def get_usage_service():
    return UsageService(
        MongoDbClient(),
        LlmGatewayService(LlmGatewayClient())
        )

@router.post("/modelRun", response_model=UsageResponseDto)
async def start_new_model_run(
    request: UsageRequestDto,
    usage_service: UsageService = Depends(get_usage_service)
):
    result = await usage_service.create_usage_response(request.text, request.entity_classes, request.llm_id)
    return {"result": result}

@router.get("/modelRuns", response_model=AllUsagesResponseDto)
def get_all_model_runs(
    usage_service: UsageService = Depends(get_usage_service)
):
    result = usage_service.get_all_model_runs()
    return {"result": result}

@router.get("/modelRun/{model_run_id}", response_model=UsageResponseDto)
def get_model_run_by_id(
    model_run_id: str,
    usage_service: UsageService = Depends(get_usage_service)
):
    result = usage_service.get_model_run_by_id(model_run_id)
    return {"result": result}