# ============================================================================
# END-TO-END TESTS
# ============================================================================

class TestEndToEndWorkflow:
    """Complete End to End Tests"""
    
    def test_complete_workflow(self, client, test_db_client, sample_evaluation_request):
        runs_created = []
        for i in range(3):
            response = client.post("/api/modelEvaluation", json=sample_evaluation_request)
            assert response.status_code == 200
            runs_created.append(response.json()["result"]["_id"])
        
        all_runs = client.get("/api/modelEvaluations")
        assert len(all_runs.json()["result"]) == 3
        
        for run_id in runs_created:
            single_run = client.get(f"/api/modelEvaluation/{run_id}")
            assert single_run.status_code == 200
            assert single_run.json()["result"]["_id"] == run_id
        
        db_count = test_db_client.evaluation_collection.count_documents({})
        assert db_count == 3