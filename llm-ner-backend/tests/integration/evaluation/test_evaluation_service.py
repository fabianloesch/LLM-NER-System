import pytest
from app.services.evaluation_service import EvaluationService

# ============================================================================
# INTEGRATION TESTS - SERVICE LAYER
# ============================================================================

class TestEvaluationServiceIntegration:
    """Tests for EvaluationService with DB"""
    
    @pytest.mark.asyncio
    async def test_create_evaluation_response_integration(
        self, 
        test_db_client, 
        mock_openrouter_service,
        sample_evaluation_request
    ):
        service = EvaluationService(test_db_client, mock_openrouter_service)
        
        result = await service.create_evaluation_response(
            corpus = sample_evaluation_request["corpus"],
            llm_ids = sample_evaluation_request["llm_ids"]
        )
        
        assert result["models"] == sample_evaluation_request["llm_ids"]
        assert result["corpus"] == sample_evaluation_request["corpus"]
        assert "_id" in result
        
        db_count = test_db_client.evaluation_collection.count_documents({})
        assert db_count == 1
    
    def test_get_evaluation_by_id_direct(self, test_db_client, sample_evaluation_db_entry):
        service = EvaluationService(test_db_client)
        
        inserted = test_db_client.insert_one(
            test_db_client.evaluation_collection,
            sample_evaluation_db_entry
            )
        
        result = service.get_model_evaluation_by_id(inserted["_id"])
        
        assert result is not None
        assert result["_id"] == inserted["_id"]