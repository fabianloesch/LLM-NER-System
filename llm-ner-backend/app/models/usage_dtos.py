from pydantic import BaseModel, Field
from datetime import datetime

# Response
class Entity(BaseModel):
    start: int
    end: int
    label: str
    entity: str | None = None

class NerUsageRun(BaseModel):
    id: str = Field(alias="_id")
    created_datetime_utc: str
    text: str
    labels: list[str]
    model: str
    entities: list[Entity]

class UsageResponseDto(BaseModel):
    result: NerUsageRun

class NerUsageRunShort(BaseModel):
    id: str = Field(alias="_id")
    created_datetime_utc: str
    model: str

class AllUsagesResponseDto(BaseModel):
    result: list[NerUsageRunShort]


# Request
class UsageRequestDto(BaseModel):
    text: str
    entity_classes: list
    llm_id: str