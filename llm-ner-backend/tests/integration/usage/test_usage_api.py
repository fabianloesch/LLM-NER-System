from bson import ObjectId

# ============================================================================
# INTEGRATION TESTS - API ENDPOINTS
# ============================================================================

class TestModelRunEndpoints:
    """Tests for POST /modelRun Endpoint"""
    
    def test_create_model_run_success(
        self, 
        client, 
        mock_llm_gateway_service,
        sample_usage_run_request
    ):
        response = client.post("/api/modelRun", json=sample_usage_run_request)
        
        assert response.status_code == 200
        result = response.json()["result"]
        
        assert result["text"] == sample_usage_run_request["text"]
        assert result["entity_classes"] == sample_usage_run_request["entity_classes"]
        assert result["model"] == sample_usage_run_request["llm_id"]
        assert "entities" in result
        assert "_id" in result
        assert "created_datetime_utc" in result
        
        # OpenRouter should be called
        mock_llm_gateway_service.run_ner_model.assert_called_once_with(
            sample_usage_run_request["text"],
            sample_usage_run_request["entity_classes"],
            sample_usage_run_request["llm_id"]
        )
    
    def test_create_model_run_stores_in_database(
        self, 
        client, 
        test_db_client,
        sample_usage_run_request
    ):
        response = client.post("/api/modelRun", json=sample_usage_run_request)
        result_id = response.json()["result"]["_id"]
        
        db_entry = test_db_client.usage_collection.find_one(
            {"_id": ObjectId(result_id)}
        )
        
        assert db_entry is not None
        assert db_entry["text"] == sample_usage_run_request["text"]
        assert db_entry["model"] == sample_usage_run_request["llm_id"]
        assert "created_datetime_utc" in db_entry
    
    def test_create_model_run_invalid_data(self, client):
        invalid_request = {
            "text": "Test",
            # entity_classes is missing
            "llm_id": "test-model"
        }
        
        response = client.post("/api/modelRun", json=invalid_request)
        assert response.status_code == 422  # Validation Error
    
    def test_create_model_run_empty_text(self, client):
        """Test: Leerer Text wird verarbeitet"""
        request_data = {
            "text": "",
            "entity_classes": ["Test"],
            "llm_id": "test-model"
        }
        
        response = client.post("/api/modelRun", json=request_data)
        assert response.status_code == 200


class TestGetModelRunsEndpoints:
    """Tests for GET Endpoints"""
    
    def test_get_all_model_runs_empty(self, client):
        response = client.get("/api/modelRuns")
        
        assert response.status_code == 200
        assert response.json()["result"] == []
    
    def test_get_all_model_runs_with_data(self, client, test_db_client):
        test_runs = [
            {
                "text": f"Test {i}",
                "entity_classes": ["Entity"],
                "model": f"model-{i}",
                "entities": []
            }
            for i in range(3)
        ]
        
        for run in test_runs:
            test_db_client.insert_one(test_db_client.usage_collection, run)
        
        response = client.get("/api/modelRuns")
        
        assert response.status_code == 200
        result = response.json()["result"]
        assert len(result) == 3
        
        # only projection should be returned
        for item in result:
            assert "_id" in item
            assert "model" in item
            assert "created_datetime_utc" in item
            assert "text" not in item  # should not be in projection
    
    def test_get_model_run_by_id_success(self, client, test_db_client):
        test_run = {
            "text": "Spezifischer Test",
            "entity_classes": ["TestEntity"],
            "model": "test-model-id",
            "entities": [{"start": 0, "end": 4, "label": "TestClass", "entity": "Test"}]
        }
        
        inserted = test_db_client.insert_one(
            test_db_client.usage_collection,
            test_run
        )
        run_id = inserted["_id"]
        
        response = client.get(f"/api/modelRun/{run_id}")
        
        assert response.status_code == 200
        result = response.json()["result"]
        assert result["_id"] == run_id
        assert result["text"] == test_run["text"]
        assert result["entities"] == test_run["entities"]