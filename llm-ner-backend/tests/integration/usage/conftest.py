import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.usage_router import get_usage_service
from app.services.usage_service import UsageService

# ============================================================================
# TEST-SPEZIFISCHE FIXTURES
# ============================================================================

@pytest.fixture
def test_usage_service(test_db_client, mock_openrouter_service):
    """Erstellt einen UsageService mit Test-Dependencies"""
    return UsageService(
        mongo_db_client=test_db_client,
        openrouter_service=mock_openrouter_service
    )


@pytest.fixture
def client(test_usage_service):
    """FastAPI TestClient mit überschriebenen Dependencies"""
    def override_get_usage_service():
        return test_usage_service
    
    app.dependency_overrides[get_usage_service] = override_get_usage_service
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()