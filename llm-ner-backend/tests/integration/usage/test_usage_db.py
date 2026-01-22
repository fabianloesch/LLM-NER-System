from bson import ObjectId

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