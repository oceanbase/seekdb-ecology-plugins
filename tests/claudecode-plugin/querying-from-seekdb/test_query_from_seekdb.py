"""Tests for query_from_seekdb module."""
import os
import tempfile
import pytest

from query_from_seekdb import (
    client,
    get_collection,
    query_by_text,
    get_by_ids,
    get_all,
    hybrid_search,
    results_to_dataframe,
    export_to_file,
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


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test output files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_get_collection(setup_test_collection):
    """Test getting an existing collection."""
    collection = get_collection(TEST_COLLECTION)
    assert collection is not None
    assert collection.count() == 5


def test_get_collection_not_found():
    """Test getting a non-existent collection raises error."""
    with pytest.raises(ValueError, match="not found"):
        get_collection("non_existent_collection")


def test_query_by_text(setup_test_collection):
    """Test semantic similarity search."""
    results = query_by_text(
        collection_name=TEST_COLLECTION,
        query_text="artificial intelligence and machine learning",
        n_results=3
    )
    
    assert "ids" in results
    assert len(results["ids"]) > 0
    assert len(results["ids"][0]) <= 3
    # First result should be about AI/ML
    assert "doc1" in results["ids"][0] or "doc4" in results["ids"][0]


def test_query_by_text_with_metadata_filter(setup_test_collection):
    """Test semantic search with metadata filter."""
    results = query_by_text(
        collection_name=TEST_COLLECTION,
        query_text="technology and computing",
        where={"category": {"$eq": "AI"}},
        n_results=5
    )
    
    assert "ids" in results
    # All results should be from AI category
    for i, id_ in enumerate(results["ids"][0]):
        assert results["metadatas"][0][i]["category"] == "AI"


def test_query_by_text_with_document_filter(setup_test_collection):
    """Test semantic search with document filter."""
    results = query_by_text(
        collection_name=TEST_COLLECTION,
        query_text="programming",
        where_document={"$contains": "Python"},
        n_results=5
    )
    
    assert "ids" in results
    if results["ids"][0]:
        # Results should contain "Python" in document
        assert "doc2" in results["ids"][0]


def test_get_by_ids(setup_test_collection):
    """Test retrieving records by IDs."""
    results = get_by_ids(
        collection_name=TEST_COLLECTION,
        ids=["doc1", "doc3"]
    )
    
    assert "ids" in results
    assert len(results["ids"]) == 2
    assert "doc1" in results["ids"]
    assert "doc3" in results["ids"]


def test_get_all(setup_test_collection):
    """Test retrieving all records."""
    results = get_all(
        collection_name=TEST_COLLECTION,
        limit=10
    )
    
    assert "ids" in results
    assert len(results["ids"]) == 5


def test_get_all_with_pagination(setup_test_collection):
    """Test retrieving records with pagination."""
    results = get_all(
        collection_name=TEST_COLLECTION,
        limit=2,
        offset=0
    )
    
    assert "ids" in results
    assert len(results["ids"]) == 2


def test_get_all_with_filter(setup_test_collection):
    """Test retrieving records with metadata filter."""
    results = get_all(
        collection_name=TEST_COLLECTION,
        where={"score": {"$gte": 90}},
        limit=10
    )
    
    assert "ids" in results
    # Should return records with score >= 90
    for i, _ in enumerate(results["ids"]):
        assert results["metadatas"][i]["score"] >= 90


def test_hybrid_search(setup_test_collection):
    """Test hybrid search combining full-text and vector search."""
    results = hybrid_search(
        collection_name=TEST_COLLECTION,
        query_text="machine learning AI",
        contains="artificial",
        n_results=3
    )
    
    assert "ids" in results
    # Should find the ML/AI document
    if results["ids"] and results["ids"][0]:
        assert len(results["ids"][0]) <= 3


# Export functionality tests

def test_results_to_dataframe_query(setup_test_collection):
    """Test converting query results to DataFrame."""
    import pandas as pd
    
    results = query_by_text(
        collection_name=TEST_COLLECTION,
        query_text="artificial intelligence",
        n_results=3
    )
    
    df = results_to_dataframe(results, result_type="query")
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) <= 3
    assert "id" in df.columns
    assert "distance" in df.columns


def test_results_to_dataframe_get(setup_test_collection):
    """Test converting get results to DataFrame."""
    import pandas as pd
    
    results = get_all(
        collection_name=TEST_COLLECTION,
        limit=5
    )
    
    df = results_to_dataframe(results, result_type="get")
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert "id" in df.columns
    assert "category" in df.columns
    assert "score" in df.columns


def test_results_to_dataframe_empty():
    """Test converting empty results to DataFrame."""
    import pandas as pd
    
    empty_results = {"ids": [], "documents": [], "metadatas": []}
    
    df = results_to_dataframe(empty_results, result_type="get")
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_export_to_csv(setup_test_collection, temp_dir):
    """Test exporting DataFrame to CSV."""
    import pandas as pd
    
    results = get_all(collection_name=TEST_COLLECTION, limit=5)
    df = results_to_dataframe(results, result_type="get")
    
    output_path = os.path.join(temp_dir, "test_export.csv")
    abs_path = export_to_file(df, output_path)
    
    assert os.path.exists(abs_path)
    
    # Verify content
    read_df = pd.read_csv(abs_path)
    assert len(read_df) == 5
    assert "id" in read_df.columns


def test_export_to_excel(setup_test_collection, temp_dir):
    """Test exporting DataFrame to Excel."""
    import pandas as pd
    
    results = get_all(collection_name=TEST_COLLECTION, limit=5)
    df = results_to_dataframe(results, result_type="get")
    
    output_path = os.path.join(temp_dir, "test_export.xlsx")
    abs_path = export_to_file(df, output_path, sheet_name="TestData")
    
    assert os.path.exists(abs_path)
    
    # Verify content
    read_df = pd.read_excel(abs_path, sheet_name="TestData")
    assert len(read_df) == 5
    assert "id" in read_df.columns


def test_export_to_invalid_format(setup_test_collection, temp_dir):
    """Test exporting to invalid format raises error."""
    import pandas as pd
    
    results = get_all(collection_name=TEST_COLLECTION, limit=5)
    df = results_to_dataframe(results, result_type="get")
    
    output_path = os.path.join(temp_dir, "test_export.txt")
    
    with pytest.raises(ValueError, match="Unsupported file format"):
        export_to_file(df, output_path)


def test_export_creates_parent_directories(setup_test_collection, temp_dir):
    """Test that export creates parent directories if needed."""
    import pandas as pd
    
    results = get_all(collection_name=TEST_COLLECTION, limit=5)
    df = results_to_dataframe(results, result_type="get")
    
    output_path = os.path.join(temp_dir, "nested", "dir", "export.csv")
    abs_path = export_to_file(df, output_path)
    
    assert os.path.exists(abs_path)


def test_export_preserves_metadata_columns(setup_test_collection, temp_dir):
    """Test that all metadata columns are preserved in export."""
    import pandas as pd
    
    results = get_all(collection_name=TEST_COLLECTION, limit=5)
    df = results_to_dataframe(results, result_type="get")
    
    output_path = os.path.join(temp_dir, "metadata_export.csv")
    abs_path = export_to_file(df, output_path)
    
    read_df = pd.read_csv(abs_path)
    
    # Check all metadata columns exist
    assert "category" in read_df.columns
    assert "score" in read_df.columns
    assert "year" in read_df.columns
    assert "document" in read_df.columns
