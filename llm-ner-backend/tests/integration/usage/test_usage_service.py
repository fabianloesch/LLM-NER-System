import pytest
from app.services.usage_service import UsageService

# ============================================================================
# INTEGRATION TESTS - SERVICE LAYER
# ============================================================================

class TestUsageServiceIntegration:
    """Direkte Tests für den UsageService mit echter DB"""
    
    @pytest.mark.asyncio
    async def test_create_usage_response_integration(
        self, 
        test_db_client, 
        mock_openrouter_service,
        sample_usage_data
    ):
        """Test: Vollständiger Durchlauf der create_usage_response Methode"""
        service = UsageService(test_db_client, mock_openrouter_service)
        
        result = await service.create_usage_response(
            text=sample_usage_data["text"],
            entity_classes=sample_usage_data["entity_classes"],
            llm_id=sample_usage_data["llm_id"]
        )
        
        # Überprüfe Rückgabewert
        assert result["text"] == sample_usage_data["text"]
        assert result["model"] == sample_usage_data["llm_id"]
        assert "_id" in result
        
        # Überprüfe Datenbankinhalt
        db_count = test_db_client.usage_collection.count_documents({})
        assert db_count == 1
    
    @pytest.mark.asyncio
    async def test_create_usage_response_with_entities(
        self, 
        test_db_client, 
        mock_openrouter_service,
        sample_entities
    ):
        """Test: Entities werden korrekt gespeichert"""
        # Konfiguriere Mock mit spezifischen Entities
        mock_openrouter_service.run_ner_model.return_value = {
            "model": "test-model",
            "identifier": None,
            "response": sample_entities
        }
        
        service = UsageService(test_db_client, mock_openrouter_service)
        
        result = await service.create_usage_response(
            text="Test",
            entity_classes=["Medication"],
            llm_id="test-model"
        )
        
        assert result["entities"] == sample_entities
    
    def test_get_all_model_runs_with_filter(self, test_db_client):
        """Test: Filtern von Model Runs"""
        service = UsageService(test_db_client)
        
        # Erstelle Test-Daten mit unterschiedlichen Models
        test_db_client.insert_one(test_db_client.usage_collection, {
            "text": "Test 1",
            "model": "model-a",
            "entity_classes": [],
            "entities": []
        })
        test_db_client.insert_one(test_db_client.usage_collection, {
            "text": "Test 2",
            "model": "model-b",
            "entity_classes": [],
            "entities": []
        })
        
        # Filter nur für model-a
        result = service.get_all_model_runs(filter={"model": "model-a"})
        
        assert len(result) == 1
        assert result[0]["model"] == "model-a"
    
    def test_get_model_run_by_id_direct(self, test_db_client):
        """Test: Direktes Abrufen über Service"""
        service = UsageService(test_db_client)
        
        inserted = test_db_client.insert_one(test_db_client.usage_collection, {
            "text": "Direct Test",
            "model": "test",
            "entity_classes": [],
            "entities": []
        })
        
        result = service.get_model_run_by_id(inserted["_id"])
        
        assert result is not None
        assert result["text"] == "Direct Test"