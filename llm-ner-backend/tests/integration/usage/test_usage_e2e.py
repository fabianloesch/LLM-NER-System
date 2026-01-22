# ============================================================================
# END-TO-END TESTS
# ============================================================================

class TestEndToEndWorkflow:
    """Vollständige End-to-End Tests"""
    
    def test_complete_workflow(self, client, test_db_client, sample_usage_data):
        """Test: Kompletter Workflow von Erstellung bis Abruf"""
        # 1. Erstelle mehrere Model Runs
        runs_created = []
        for i in range(3):
            data = sample_usage_data.copy()
            data["text"] = f"Workflow Test {i}"
            data["llm_id"] = f"model-{i}"
            
            response = client.post("/api/modelRun", json=data)
            assert response.status_code == 200
            runs_created.append(response.json()["result"]["_id"])
        
        # 2. Hole alle Model Runs
        all_runs = client.get("/api/modelRuns")
        assert len(all_runs.json()["result"]) == 3
        
        # 3. Hole jeden einzelnen Run
        for run_id in runs_created:
            single_run = client.get(f"/api/modelRun/{run_id}")
            assert single_run.status_code == 200
            assert single_run.json()["result"]["_id"] == run_id
        
        # 4. Überprüfe Datenbankinhalt
        db_count = test_db_client.usage_collection.count_documents({})
        assert db_count == 3
    
    def test_workflow_with_different_entity_classes(
        self, 
        client, 
        sample_usage_data
    ):
        """Test: Workflow mit verschiedenen Entity-Klassen"""
        entity_class_sets = [
            ["Medication"],
            ["Medication", "Indication"],
            ["Medication", "Indication", "Dosage"]
        ]
        
        for entity_classes in entity_class_sets:
            data = sample_usage_data.copy()
            data["entity_classes"] = entity_classes
            
            response = client.post("/api/modelRun", json=data)
            assert response.status_code == 200
            
            result = response.json()["result"]
            assert result["entity_classes"] == entity_classes