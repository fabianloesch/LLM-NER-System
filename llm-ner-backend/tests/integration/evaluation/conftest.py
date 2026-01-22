import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.evaluation_router import get_evaluation_service
from app.services.evaluation_service import EvaluationService

# ============================================================================
# TEST-SPECIFIC FIXTURES
# ============================================================================

@pytest.fixture
def test_evaluation_service(test_db_client, mock_openrouter_service):
    """EvaluationService with Test Dependencies"""
    return EvaluationService(
        mongo_db_client=test_db_client,
        openrouter_service=mock_openrouter_service
    )


@pytest.fixture
def client(test_evaluation_service):
    """FastAPI TestClient with overridden Dependencies"""
    def override_get_evaluation_service():
        return test_evaluation_service
    
    app.dependency_overrides[get_evaluation_service] = override_get_evaluation_service
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()

# ============================================================================
# HELPER FIXTURES
# ============================================================================

@pytest.fixture
def sample_corpus():
    return [
            {
                "id": 1,
                "text": "Der Patient sollte bei Asthma bronchiale Formoterol/Beclometason 6/100 µg als Dosieraerosol morgens und abends inhalativ versuchen.",
                "label": [
                [41, 64, "Drug"],
                [65, 73, "Strength"],
                [78, 91, "Form"],
                [92, 110, "Frequency"],
                [111, 120, "Form"]
                ]
            },
            {
                "id": 2,
                "text": "Wegen Ihrer erhöhten Zucker-Werte ist neben Metformin 1000 mg zweimal täglich auch Empagliflozin 10 mg einmal täglich - beides als Tablette - erforderlich.",
                "label": [
                [44, 53, "Drug"],
                [54, 61, "Strength"],
                [62, 77, "Frequency"],
                [83, 96, "Drug"],
                [97, 102, "Strength"],
                [103, 117, "Frequency"],
                [131, 139, "Form"]
                ]
            }
        ]

@pytest.fixture
def sample_evaluation_db_entry(sample_corpus):
    return {
        "models": ["m1", "m2"],
        "entity_classes": ["E1", "E2"],
        "evaluations":{
            "m1":{
                "overall": {
                    "precision": 1,
                    "recall": 1,
                    "f1_score": 1,
                },
                "entityClassLevel": {
                    "E1": {
                    "precision": 1,
                    "recall": 1,
                    "f1_score": 1,
                    },
                    "E2": {
                        "precision": 1,
                        "recall": 1,
                        "f1_score": 1,
                    }
                }
            },
            "m2":{
                "overall": {
                    "precision": 1,
                    "recall": 1,
                    "f1_score": 1,
                },
                "entityClassLevel": {
                    "E1": {
                    "precision": 1,
                    "recall": 1,
                    "f1_score": 1,
                    },
                    "E2": {
                        "precision": 1,
                        "recall": 1,
                        "f1_score": 1,
                    }
                }
            },
        },
        "corpus": sample_corpus
    }

@pytest.fixture
def sample_evaluation_request(sample_corpus):
    """
    Beispiel-Daten für Usage-Tests.
    Kann in Tests einfach wiederverwendet werden.
    """
    return {
        "llm_ids": ["test-model-1", "test-model-2"],
        "corpus": sample_corpus
    }