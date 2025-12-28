from typing import List, Tuple
from pydantic import BaseModel

class Metrics(BaseModel):
    precision: float
    recall: float
    f1_score: float

class MetricLevels(BaseModel):
    overall: Metrics
    entityClassLevel: dict[str, Metrics]

class EvaluationResponseDto(BaseModel):
    result: dict[str, MetricLevels]

Entity = Tuple[int, int, str]

class CorpusEntry(BaseModel):
    id: int
    text: str
    label: list[Entity]

class EvaluationRequestDto(BaseModel):
    corpus: list[CorpusEntry]
    llm_ids: list[str]