"""Tests for query_from_seekdb module."""
import pytest

from query_from_seekdb import (
    client,
    get_collection,
    get_by_filter,
    hybrid_search,
    list_collections,
    collection_info

)


# Test collection name
TEST_COLLECTION = "test_query_collection"


@pytest.fixture(scope="module")
def setup_test_collection():
    """Create and populate a test collection for querying."""
    # Clean up if exists
    if client.has_collection(TEST_COLLECTION):
        client.delete_collection(TEST_COLLECTION)

    # Create collection with default embedding function
    collection = client.get_or_create_collection(name=TEST_COLLECTION)

    # Add test data
    documents = [
        "Machine learning is a subset of artificial intelligence",
        "Python is a popular programming language for data science",
        "Vector databases enable semantic search capabilities",
        "Neural networks are inspired by the human brain structure",
        "Natural language processing helps computers understand text",
    ]

    ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]

    metadatas = [
        {"category": "AI", "score": 95, "year": 2023},
        {"category": "Programming", "score": 88, "year": 2022},
        {"category": "Database", "score": 92, "year": 2024},
        {"category": "AI", "score": 90, "year": 2023},
        {"category": "NLP", "score": 85, "year": 2021},
    ]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)

    yield collection

    # Cleanup
    client.delete_collection(TEST_COLLECTION)


def test_get_collection(setup_test_collection):
    """Test getting an existing collection."""
    collection = get_collection(TEST_COLLECTION)
    assert collection is not None
    assert collection.count() == 5


def test_get_by_filter_scalar(setup_test_collection):
    """Test filtering documents by scalar metadata field."""
    where = {"category": "AI"}
    result = get_by_filter(collection_name=TEST_COLLECTION, where=where)
    assert set(result["ids"][0]) == {"doc1", "doc4"}


def test_hybrid_search_fulltext_semantic(setup_test_collection):
    query_text = "Vector databases"
    result = hybrid_search(collection_name=TEST_COLLECTION,
                           query_text=query_text, n_results=1)
    assert set(result["ids"][0]) == {"doc3"}


def test_hybrid_search_fulltext_semantic_scalar(setup_test_collection):
    query_text = "Machine learning"
    where = {"category": "AI", "score": 90}
    result = hybrid_search(collection_name=TEST_COLLECTION,
                           query_text=query_text, where=where, n_results=1)
    assert set(result["ids"][0]) == {"doc4"}

def test_list_collections(setup_test_collection):
    """Test listing all collections."""
    collections = list_collections()
    assert collections is not None
    assert len(collections) > 0
    collection_names = [col.name if hasattr(col, 'name') else str(col) for col in collections]
    assert TEST_COLLECTION in collection_names

def test_collection_info(setup_test_collection):
    """Test getting collection info."""
    info = collection_info(TEST_COLLECTION)
    assert info is not None
    assert info["name"] == TEST_COLLECTION
    assert info["count"] == 5
    assert info["preview"] is not None
    assert len(info["preview"]["ids"]) == 3