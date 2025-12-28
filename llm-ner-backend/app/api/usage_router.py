from fastapi import APIRouter, Depends
from app.models.usage_dtos import UsageResponseDto
from app.models.usage_dtos import UsageRequestDto
from app.openrouter.openrouter_service import OpenRouterService
from app.openrouter.openrouter_client import OpenRouterClient
from app.services.usage_service import UsageService

router = APIRouter()

def get_usage_service():
    return UsageService(OpenRouterService(OpenRouterClient()))

@router.post("/modelRun", response_model=UsageResponseDto)
def start_new_model_run(
    request: UsageRequestDto,
    usage_service: UsageService = Depends(get_usage_service)
):
    result = usage_service.create_ner_response(request.text, request.entity_classes, request.llm_id)
    return {"result": result}

@router.get("/modelRuns")
def get_all_model_runs(
    usage_service: UsageService = Depends(get_usage_service)
):
    raise NotImplementedError

@router.get("/modelRun/{model_run_id}")
def get_model_run_by_id(
    model_run_id: int,
    usage_service: UsageService = Depends(get_usage_service)
):
    raise NotImplementedError