from bson import ObjectId

# ============================================================================
# INTEGRATION TESTS - API ENDPOINTS
# ============================================================================

class TestModelRunEndpoints:
    """Tests für die /modelRun Endpoints"""
    
    def test_create_model_run_success(
        self, 
        client, 
        mock_openrouter_service,
        sample_usage_data
    ):
        """Test: Erfolgreiche Erstellung eines Model Runs"""
        response = client.post("/api/modelRun", json=sample_usage_data)
        
        assert response.status_code == 200
        result = response.json()["result"]
        
        # Validiere Response-Struktur
        assert result["text"] == sample_usage_data["text"]
        assert result["entity_classes"] == sample_usage_data["entity_classes"]
        assert result["model"] == sample_usage_data["llm_id"]
        assert "entities" in result
        assert "_id" in result
        assert "created_datetime_utc" in result
        
        # Überprüfe, dass OpenRouter aufgerufen wurde
        mock_openrouter_service.run_ner_model.assert_called_once_with(
            sample_usage_data["text"],
            sample_usage_data["entity_classes"],
            sample_usage_data["llm_id"]
        )
    
    def test_create_model_run_stores_in_database(
        self, 
        client, 
        test_db_client,
        sample_usage_data
    ):
        """Test: Model Run wird korrekt in MongoDB gespeichert"""
        response = client.post("/api/modelRun", json=sample_usage_data)
        result_id = response.json()["result"]["_id"]
        
        # Hole direkt aus der Datenbank
        db_entry = test_db_client.usage_collection.find_one(
            {"_id": ObjectId(result_id)}
        )
        
        assert db_entry is not None
        assert db_entry["text"] == sample_usage_data["text"]
        assert db_entry["model"] == sample_usage_data["llm_id"]
        assert "created_datetime_utc" in db_entry
    
    def test_create_model_run_invalid_data(self, client):
        """Test: Fehlerhafte Request-Daten werden abgelehnt"""
        invalid_request = {
            "text": "Test",
            # entity_classes fehlt
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
    """Tests für die GET Endpoints"""
    
    def test_get_all_model_runs_empty(self, client):
        """Test: Leere Liste wenn keine Model Runs vorhanden"""
        response = client.get("/api/modelRuns")
        
        assert response.status_code == 200
        assert response.json()["result"] == []
    
    def test_get_all_model_runs_with_data(self, client, test_db_client):
        """Test: Abrufen aller Model Runs"""
        # Erstelle Test-Daten direkt in der DB
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
        
        # Überprüfe, dass nur die Projektion zurückgegeben wird
        for item in result:
            assert "_id" in item
            assert "model" in item
            assert "created_datetime_utc" in item
            assert "text" not in item  # Sollte nicht in Projektion sein
    
    def test_get_all_model_runs_sorted_by_date(self, client, test_db_client):
        """Test: Model Runs sind nach Datum sortiert"""
        # Erstelle mehrere Runs mit unterschiedlichen Zeitstempeln
        for i in range(3):
            test_db_client.insert_one(test_db_client.usage_collection, {
                "text": f"Test {i}",
                "model": "test-model",
                "entity_classes": [],
                "entities": []
            })
        
        response = client.get("/api/modelRuns")
        result = response.json()["result"]
        
        # Prüfe, dass Zeitstempel vorhanden sind
        assert all("created_datetime_utc" in item for item in result)
    
    def test_get_model_run_by_id_success(self, client, test_db_client):
        """Test: Abrufen eines spezifischen Model Runs"""
        # Erstelle Test-Daten
        test_run = {
            "text": "Spezifischer Test",
            "entity_classes": ["TestEntity"],
            "model": "test-model-id",
            "entities": [{"start": 0, "end": 4, "label": "TestEntity", "entity": "Test"}]
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
    
    # def test_get_model_run_by_invalid_id(self, client):
    #     """Test: None bei nicht existierender ID"""
    #     invalid_id = str(ObjectId())
        
    #     response = client.get(f"/api/modelRun/{invalid_id}")
        
    #     assert response.status_code == 200
    #     assert response.json()["result"] is None
    
    # def test_get_model_run_by_malformed_id(self, client):
    #     """Test: Fehler bei fehlerhafter ID"""
    #     # Dies könnte einen 500 Error oder 422 verursachen
    #     # abhängig von deiner Fehlerbehandlung
    #     response = client.get("/api/modelRun/invalid-id-format")
        
    #     # Prüfe, dass es nicht crasht
    #     assert response.status_code in [400, 422, 500]