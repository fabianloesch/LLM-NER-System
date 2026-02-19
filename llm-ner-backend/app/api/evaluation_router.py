from fastapi import APIRouter, Depends
from app.models.evaluation_dtos import EvaluationRequestDto, EvaluationResponseDto, AllEvaluationsResponseDto
from app.llm_gateway.llm_gateway_service import LlmGatewayService
from app.llm_gateway.llm_gateway_client import LlmGatewayClient
from app.services.evaluation_service import EvaluationService
from app.db.mongo_db_client import MongoDbClient

router = APIRouter()

def get_evaluation_service():
    return EvaluationService(
        MongoDbClient(),
        LlmGatewayService(LlmGatewayClient())
        )

@router.post("/modelEvaluation", response_model=EvaluationResponseDto)
async def start_new_model_evaluation(
    request: EvaluationRequestDto,
    evaluation_service: EvaluationService = Depends(get_evaluation_service)
):
    request = request.model_dump()
    result = await evaluation_service.create_evaluation_response(request["corpus"], request["llm_ids"])
    return {"result": result}

@router.get("/modelEvaluations", response_model=AllEvaluationsResponseDto)
async def get_all_model_evaluations(
    evaluation_service: EvaluationService = Depends(get_evaluation_service)
):
    result = evaluation_service.get_all_model_evaluations()
    return {"result": result}

@router.get("/modelEvaluation/{model_evaluation_id}", response_model=EvaluationResponseDto)
async def get_model_evaluation_by_id(
    model_evaluation_id: str,
    evaluation_service: EvaluationService = Depends(get_evaluation_service)
):
    result = evaluation_service.get_model_evaluation_by_id(model_evaluation_id)
    return {"result": result}