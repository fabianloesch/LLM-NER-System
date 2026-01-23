"""
Gemeinsame Test-Fixtures für alle Tests
"""
import pytest
from pymongo import MongoClient
from unittest.mock import AsyncMock
import os

from app.db.mongo_db_client import MongoDbClient
from app.openrouter.openrouter_service import OpenRouterService


# ============================================================================
# SESSION-SCOPED FIXTURES (are executed once per test session)
# ============================================================================

@pytest.fixture(scope="session")
def test_mongo_client():
    connection_url = os.getenv(
        "MONGO_DB_CONNECTION_STRING",
        "mongodb://admin:password@mongodb:27017/test_db?authSource=admin"
    )
    client = MongoClient(connection_url)
    yield client
    client.close()


# ============================================================================
# FUNCTION-SCOPED FIXTURES (are executed individually for every test)
# ============================================================================

@pytest.fixture
def test_db_client(test_mongo_client):
    test_db_client = MongoDbClient()
    # Override connection with Test-DB
    test_db_client.client = test_mongo_client
    test_db_client.database = test_mongo_client.LLM_NER_SYSTEM_DB_TEST
    test_db_client.usage_collection = test_db_client.database.Usages
    test_db_client.evaluation_collection = test_db_client.database.Evaluations
    
    yield test_db_client
    
    # Cleanup
    test_db_client.database.Usages.delete_many({})
    test_db_client.database.Evaluations.delete_many({})


@pytest.fixture
def mock_openrouter_service():
    mock_service = AsyncMock(spec=OpenRouterService)
    
    # Sample return value for run_ner_model
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
    
    # Sample return value for get_available_models
    mock_service.get_available_models.return_value = [
        {
            "id": "test-model-1",
            "name": "Test Model 1",
            "createdAtUtc": "2024-01-01T00:00:00Z"
        }
    ]

    # Sample return value for run_ner_model_batch
    mock_service.run_ner_model_batch.return_value = {
            "test-model-1": 
                {
                    1: [
                            {
                                "entity": "TestEntity",
                                "label": "TestLabel",
                                "start": 0,
                                "end": 11
                            },
                            {
                                "entity": "TestEntity",
                                "label": "TestLabel",
                                "start": 12,
                                "end": 13
                            }
                        ],
                    2: [
                            {
                                "entity": "TestEntity",
                                "label": "TestLabel",
                                "start": 12,
                                "end": 13
                            }
                        ]
                },
            "test-model-2": 
                {
                    1: [
                        {
                            "entity": "TestEntity",
                            "label": "TestLabel",
                            "start": 0,
                            "end": 11
                        },
                        {
                            "entity": "TestEntity",
                            "label": "TestLabel",
                            "start": 12,
                            "end": 13
                        }],
                    2: [
                        {
                            "entity": "TestEntity",
                            "label": "TestLabel",
                            "start": 12,
                            "end": 13
                        }]
                 }
        }
    
    return mock_service
