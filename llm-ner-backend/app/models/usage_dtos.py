from pydantic import BaseModel

class UsageResponseDto(BaseModel):
    result: dict

class UsageRequestDto(BaseModel):
    text: str
    entity_classes: list
    llm_id: str