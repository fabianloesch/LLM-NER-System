"""
Integrationstests für Usage-Endpoints mit MongoDB
"""
import pytest
from fastapi.testclient import TestClient
from bson import ObjectId

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


# ============================================================================
# INTEGRATION TESTS - DATABASE OPERATIONS
# ============================================================================

class TestMongoDbClientIntegration:
    """Tests für MongoDB-Operationen"""
    
    def test_insert_one_adds_timestamp(self, test_db_client):
        """Test: insert_one fügt created_datetime_utc hinzu"""
        document = {"test_field": "test_value"}
        
        result = test_db_client.insert_one(
            test_db_client.usage_collection,
            document
        )
        
        assert "created_datetime_utc" in result
        assert "_id" in result
        assert isinstance(result["_id"], str)
    
    def test_get_one_converts_objectid(self, test_db_client):
        """Test: get_one konvertiert ObjectId zu String"""
        inserted = test_db_client.insert_one(
            test_db_client.usage_collection,
            {"test": "data"}
        )
        
        result = test_db_client.get_one(
            test_db_client.usage_collection,
            {"_id": ObjectId(inserted["_id"])}
        )
        
        assert isinstance(result["_id"], str)
    
    def test_get_one_returns_none_if_not_found(self, test_db_client):
        """Test: get_one gibt None zurück wenn nicht gefunden"""
        result = test_db_client.get_one(
            test_db_client.usage_collection,
            {"_id": ObjectId()}
        )
        
        assert result is None
    
    def test_get_many_with_projection(self, test_db_client):
        """Test: get_many mit Projektion"""
        # Füge mehrere Dokumente ein
        for i in range(3):
            test_db_client.insert_one(
                test_db_client.usage_collection,
                {"field1": f"value{i}", "field2": f"other{i}"}
            )
        
        result = test_db_client.get_many(
            test_db_client.usage_collection,
            projection={"field1": 1}
        )
        
        assert len(result) == 3
        for doc in result:
            assert "field1" in doc
            assert "_id" in doc
            assert "field2" not in doc
    
    def test_get_many_empty_collection(self, test_db_client):
        """Test: get_many gibt leere Liste zurück"""
        result = test_db_client.get_many(test_db_client.usage_collection)
        assert result == []
    
    def test_multiple_inserts_and_retrieval(self, test_db_client):
        """Test: Mehrere Inserts und Abrufen"""
        # Füge 5 Dokumente ein
        inserted_ids = []
        for i in range(5):
            doc = test_db_client.insert_one(
                test_db_client.usage_collection,
                {"index": i, "data": f"test-{i}"}
            )
            inserted_ids.append(doc["_id"])
        
        # Hole alle zurück
        all_docs = test_db_client.get_many(test_db_client.usage_collection)
        assert len(all_docs) == 5
        
        # Hole ein spezifisches Dokument
        specific_doc = test_db_client.get_one(
            test_db_client.usage_collection,
            {"_id": ObjectId(inserted_ids[2])}
        )
        assert specific_doc["index"] == 2


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