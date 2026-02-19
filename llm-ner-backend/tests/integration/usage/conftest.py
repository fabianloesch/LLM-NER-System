import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.usage_router import get_usage_service
from app.services.usage_service import UsageService

# ============================================================================
# TEST-SPECIFIC FIXTURES
# ============================================================================

@pytest.fixture
def test_usage_service(test_db_client, mock_llm_gateway_service):
    """UsageService with Test Dependencies"""
    return UsageService(
        mongo_db_client=test_db_client,
        llm_gateway_service=mock_llm_gateway_service
    )


@pytest.fixture
def client(test_usage_service):
    """FastAPI TestClient with overridden Dependencies"""
    def override_get_usage_service():
        return test_usage_service
    
    app.dependency_overrides[get_usage_service] = override_get_usage_service
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()

# ============================================================================
# HELPER FIXTURES
# ============================================================================

@pytest.fixture
def sample_usage_run_request():
    return {
        "text": "Der Patient erhält Amoxicillin gegen Bronchitis.",
        "entity_classes": ["Medication", "Indication"],
        "llm_id": "openai/gpt-4"
    }


@pytest.fixture
def sample_entities():
    """
    Beispiel-Entitäten für Tests.
    """
    return [
        {
            "entity": "Amoxicillin",
            "label": "Medication",
            "start": 20,
            "end": 31
        },
        {
            "entity": "Bronchitis",
            "label": "Indication",
            "start": 38,
            "end": 48
        }
    ]