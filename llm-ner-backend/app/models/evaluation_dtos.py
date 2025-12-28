from pydantic import BaseModel

class EvaluationResponseDto(BaseModel):
    result: dict

class EvaluationRequestDto(BaseModel):
    text: str
    entity_classes: list
    llm_id: str