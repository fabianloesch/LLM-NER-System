from bson import ObjectId
import copy

# ============================================================================
# INTEGRATION TESTS - API ENDPOINTS
# ============================================================================

class TestPostEvaluationEndpoints:
    """Tests for POST /modelEvaluation Endpoint"""
    
    def test_create_evaluation_success(
        self, 
        client, 
        mock_llm_gateway_service,
        sample_evaluation_request
    ):
        response = client.post("/api/modelEvaluation", json=sample_evaluation_request)
        
        assert response.status_code == 200
        result = response.json()["result"]
        
        assert result["models"] == sample_evaluation_request["llm_ids"]
        assert result["corpus"] == sample_evaluation_request["corpus"]
        assert "entity_classes" in result
        assert "_id" in result
        assert "created_datetime_utc" in result
        assert "evaluations" in result
        
        mock_llm_gateway_service.run_ner_model_batch.assert_called_once()
    
    def test_create_evaluation_stores_in_database(
        self, 
        client, 
        test_db_client,
        sample_evaluation_request
    ):
        response = client.post("/api/modelEvaluation", json=sample_evaluation_request)
        result_id = response.json()["result"]["_id"]
        
        db_entry = test_db_client.evaluation_collection.find_one(
            {"_id": ObjectId(result_id)}
        )
        
        assert db_entry is not None
        assert db_entry["corpus"] == sample_evaluation_request["corpus"]
        assert db_entry["models"] == sample_evaluation_request["llm_ids"]
        assert "entity_classes" in db_entry
        assert "evaluations" in db_entry
        assert "created_datetime_utc" in db_entry
    
    def test_create_evaluation_invalid_data(self, client):
        invalid_request = {
            "corpus": {}, # corpus empty
            "llm_ids": ["m1", "m2"]
        }
        
        response = client.post("/api/modelEvaluation", json=invalid_request)
        assert response.status_code == 422  # Validation Error


class TestGetEvaluationsEndpoints:
    
    def test_get_all_evaluations_empty(self, client):
        response = client.get("/api/modelEvaluations")
        
        assert response.status_code == 200
        assert response.json()["result"] == []
    
    def test_get_all_evaluations_with_data(self, client, test_db_client, sample_evaluation_db_entry):
        for i in range(3):
            db_entry = copy.deepcopy(sample_evaluation_db_entry)
            test_db_client.insert_one(test_db_client.evaluation_collection, db_entry)
        
        response = client.get("/api/modelEvaluations")
        
        assert response.status_code == 200
        result = response.json()["result"]
        assert len(result) == 3
        
        for item in result:
            assert "_id" in item
            assert "created_datetime_utc" in item
            assert "models" in item
            assert "entity_classes" not in item
            assert "evaluations" not in item  # should not be in projection
            assert "corpus" not in item  # should not be in projection
    
    def test_get_evaluation_by_id_success(self, client, test_db_client, sample_evaluation_db_entry):
        inserted = test_db_client.insert_one(
            test_db_client.evaluation_collection,
            sample_evaluation_db_entry
        )
        evaluation_id = inserted["_id"]
        
        response = client.get(f"/api/modelEvaluation/{evaluation_id}")
        
        assert response.status_code == 200
        result = response.json()["result"]
        assert result["_id"] == evaluation_id