"""
Gemeinsame Test-Fixtures für alle Tests
"""
import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from unittest.mock import AsyncMock

from app.db.mongo_db_client import MongoDbClient
from app.openrouter.openrouter_service import OpenRouterService


# ============================================================================
# SESSION-SCOPED FIXTURES (werden einmal pro Test-Session erstellt)
# ============================================================================

@pytest.fixture(scope="session")
def mongo_container():
    """
    Startet einen MongoDB-Container für die gesamte Test-Session.
    Wird nur einmal gestartet und von allen Tests wiederverwendet.
    """
    with MongoDbContainer("mongo:7.0") as container:
        yield container


@pytest.fixture(scope="session")
def test_mongo_client(mongo_container):
    """
    Erstellt einen MongoDB-Client für die Test-Datenbank.
    Wird für die gesamte Session wiederverwendet.
    """
    connection_url = mongo_container.get_connection_url()
    client = MongoClient(connection_url)
    yield client
    client.close()


# ============================================================================
# FUNCTION-SCOPED FIXTURES (werden für jeden Test neu erstellt)
# ============================================================================

@pytest.fixture
def test_db_client(test_mongo_client):
    """
    Erstellt einen Test-MongoDbClient mit der Test-Datenbank.
    Nach jedem Test werden alle Collections geleert (Cleanup).
    """
    test_db_client = MongoDbClient()
    # Überschreibe die Verbindung mit der Test-DB
    test_db_client.client = test_mongo_client
    test_db_client.database = test_mongo_client.LLM_NER_SYSTEM_DB_TEST
    test_db_client.usage_collection = test_db_client.database.Usages
    test_db_client.evaluation_collection = test_db_client.database.Evaluations
    
    yield test_db_client
    
    # Cleanup: Lösche alle Daten nach jedem Test
    test_db_client.database.Usages.delete_many({})
    test_db_client.database.Evaluations.delete_many({})


@pytest.fixture
def mock_openrouter_service():
    """
    Mock für den OpenRouterService.
    Verhindert echte API-Calls in Tests.
    """
    mock_service = AsyncMock(spec=OpenRouterService)
    
    # Standard-Rückgabewert für run_ner_model
    mock_service.run_ner_model.return_value = {
        "model": "test-model",
        "identifier": None,
        "response": [
            {
                "entity": "TestEntity",
                "label": "TestLabel",
                "start": 0,
                "end": 11
            }
        ]
    }
    
    # Standard-Rückgabewert für get_available_models
    mock_service.get_available_models.return_value = [
        {
            "id": "test-model-1",
            "name": "Test Model 1",
            "createdAtUtc": "2024-01-01T00:00:00Z"
        }
    ]
    
    return mock_service


# ============================================================================
# HELPER FIXTURES
# ============================================================================

@pytest.fixture
def sample_usage_data():
    """
    Beispiel-Daten für Usage-Tests.
    Kann in Tests einfach wiederverwendet werden.
    """
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