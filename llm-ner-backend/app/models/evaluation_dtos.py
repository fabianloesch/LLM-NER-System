from typing import Tuple
from pydantic import BaseModel, Field

# Request
Entity = Tuple[int, int, str]

class CorpusEntry(BaseModel):
    id: int
    text: str
    label: list[Entity]

class EvaluationRequestDto(BaseModel):
    corpus: list[CorpusEntry]
    llm_ids: list[str]

# Response 
class Metrics(BaseModel):
    precision: float
    recall: float
    f1_score: float

class MetricLevels(BaseModel):
    overall: Metrics
    entityClassLevel: dict[str, Metrics]

class NerEvaluation(BaseModel):
    id: str = Field(alias="_id")
    created_datetime_utc: str
    models: list[str]
    entity_classes: list[str]
    evaluations: dict[str, MetricLevels]
    corpus: list[CorpusEntry]

class EvaluationResponseDto(BaseModel):
    result: NerEvaluation

class NerEvaluationShort(BaseModel):
    id: str = Field(alias="_id")
    created_datetime_utc: str
    models: list[str]

class AllEvaluationsResponseDto(BaseModel):
    result: list[NerEvaluationShort]