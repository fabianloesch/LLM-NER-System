from bson import ObjectId
import copy

# ============================================================================
# INTEGRATION TESTS - DATABASE OPERATIONS
# ============================================================================

class TestMongoDbClientIntegration:
    """Tests for MongoDB Operations"""
    
    def test_insert_one_adds_timestamp(self, test_db_client, sample_evaluation_db_entry):
        result = test_db_client.insert_one(
            test_db_client.evaluation_collection,
            sample_evaluation_db_entry
        )
        
        assert "created_datetime_utc" in result
        assert "_id" in result
        assert isinstance(result["_id"], str)
    
    def test_get_one_converts_objectid(self, test_db_client, sample_evaluation_db_entry):
        inserted = test_db_client.insert_one(
            test_db_client.evaluation_collection,
            sample_evaluation_db_entry
        )
        
        result = test_db_client.get_one(
            test_db_client.evaluation_collection,
            {"_id": ObjectId(inserted["_id"])}
        )
        
        assert isinstance(result["_id"], str)
    
    def test_get_one_returns_none_if_not_found(self, test_db_client):
        result = test_db_client.get_one(
            test_db_client.evaluation_collection,
            {"_id": ObjectId()}
        )
        
        assert result is None
    
    def test_get_many_with_projection(self, test_db_client, sample_evaluation_db_entry):
        for i in range(3):
            test_db_client.insert_one(
                test_db_client.evaluation_collection,
                copy.deepcopy(sample_evaluation_db_entry)
            )
        
        result = test_db_client.get_many(
            test_db_client.evaluation_collection,
            projection={"models": 1}
        )
        
        assert len(result) == 3
        for doc in result:
            assert "models" in doc
            assert "_id" in doc
            assert "evaluations" not in doc
    
    def test_get_many_empty_collection(self, test_db_client):
        result = test_db_client.get_many(test_db_client.evaluation_collection)
        assert result == []
    
    def test_multiple_inserts_and_retrieval(self, test_db_client, sample_evaluation_db_entry):
        inserted_ids = []
        for i in range(5):
            doc = test_db_client.insert_one(
                test_db_client.evaluation_collection,
                copy.deepcopy(sample_evaluation_db_entry)
            )
            inserted_ids.append(doc["_id"])
        
        all_docs = test_db_client.get_many(test_db_client.evaluation_collection)
        assert len(all_docs) == 5
        
        specific_doc = test_db_client.get_one(
            test_db_client.evaluation_collection,
            {"_id": ObjectId(inserted_ids[2])}
        )
        assert specific_doc["_id"] == inserted_ids[2]