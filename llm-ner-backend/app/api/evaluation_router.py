from fastapi import APIRouter, Depends
from app.models.evaluation_dtos import EvaluationRequestDto, EvaluationResponseDto
from app.openrouter.openrouter_service import OpenRouterService
from app.openrouter.openrouter_client import OpenRouterClient
from app.services.evaluation_service import EvaluationService

router = APIRouter()

def get_evaluation_service():
    return EvaluationService(OpenRouterService(OpenRouterClient()))

@router.post("/modelEvaluation", response_model=EvaluationResponseDto)
async def start_new_model_evaluation(
    request: EvaluationRequestDto,
    evaluation_service: EvaluationService = Depends(get_evaluation_service)
):
    request = request.model_dump()
    result = await evaluation_service.create_evaluation_response(request["corpus"], request["llm_ids"])
    return {"result": result}

@router.get("/modelEvaluations")
async def get_all_model_evaluations(
    evaluation_service: EvaluationService = Depends(get_evaluation_service)
):
    raise NotImplementedError

@router.get("/modelEvaluation/{model_evaluation_id}")
async def get_model_evaluation_by_id(
    model_evaluation_id: int,
    evaluation_service: EvaluationService = Depends(get_evaluation_service)
):
    raise NotImplementedError