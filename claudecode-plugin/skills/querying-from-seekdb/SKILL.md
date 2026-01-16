---
name: querying-from-seekdb
description: "Query and export data from seekdb vector database. Supports semantic similarity search, hybrid search, metadata filtering, direct retrieval, and export to CSV/Excel. When users need to: (1) Search imported data using natural language queries, (2) Perform semantic similarity search on vectorized data, (3) Combine full-text and vector search (hybrid search), (4) Retrieve records by ID or metadata filters, (5) Export query results to CSV or Excel files, or (6) Query data imported by importing-to-seekdb skill."
license: MIT
---

# Query and Export Data from seekdb

Query data from seekdb vector database with support for semantic search, hybrid search, metadata filtering, and export to CSV/Excel files.

## Prerequisites

- Python 3.10+ installed
- Data imported using the `importing-to-seekdb` skill
- Required packages:

```bash
pip install pyseekdb pandas openpyxl
```

## Quick Start

Use the provided `scripts/query_in_seekdb.py` script:

```bash
# Semantic search with text query
python scripts/query_in_seekdb.py mobiles --query-text "phone with good battery"

# Get all records from collection
python scripts/query_in_seekdb.py mobiles --get-all --limit 10

# Get specific records by IDs
python scripts/query_in_seekdb.py mobiles --get-ids "id1,id2,id3"

# List all collections
python scripts/query_in_seekdb.py --list-collections

# Export search results to CSV
python scripts/query_in_seekdb.py mobiles --query-text "phone with good battery" --output results.csv

# Export all records to Excel
python scripts/query_in_seekdb.py mobiles --get-all --limit 1000 --output mobiles.xlsx
```

## Scripts

This skill provides the following scripts in the `scripts/` directory:

| Script | Description |
|--------|-------------|
| `query_in_seekdb.py` | Main query and export script with CLI interface |

## Query Methods

### Method 1: Semantic Similarity Search (query)

Use natural language to find semantically similar documents:

```python
from scripts.query_in_seekdb import query_by_text

# Simple semantic search
results = query_by_text(
    collection_name="mobiles",
    query_text="phone with good camera and battery",
    n_results=5
)

# Search with metadata filter
results = query_by_text(
    collection_name="mobiles",
    query_text="budget smartphone",
    where={"Brand": {"$eq": "SAMSUNG"}},
    n_results=5
)

# Search with document filter
results = query_by_text(
    collection_name="mobiles",
    query_text="gaming phone",
    where_document={"$contains": "64 GB"},
    n_results=5
)
```

### Method 2: Hybrid Search

Combine full-text search and vector similarity search:

```python
from scripts.query_in_seekdb import hybrid_search

results = hybrid_search(
    collection_name="mobiles",
    query_text="smartphone with large battery",
    contains="5000 mAh",  # Full-text filter
    n_results=5,
    where={"Brand": {"$eq": "REDMI"}}
)
```

### Method 3: Direct Retrieval (get)

Retrieve records without vector search:

```python
from scripts.query_in_seekdb import get_by_ids, get_all

# Get by IDs
results = get_by_ids(
    collection_name="mobiles",
    ids=["id1", "id2", "id3"]
)

# Get all with pagination
results = get_all(
    collection_name="mobiles",
    limit=10,
    offset=0
)

# Get with metadata filter
results = get_all(
    collection_name="mobiles",
    where={"Brand": {"$eq": "SAMSUNG"}},
    limit=10
)
```

## Export to CSV/Excel

Export query results to CSV or Excel files using the `--output` option:

```bash
# Export semantic search results to CSV
python scripts/query_in_seekdb.py mobiles -q "phone with good battery" --output results.csv

# Export all records to Excel
python scripts/query_in_seekdb.py mobiles --get-all --limit 1000 --output mobiles.xlsx

# Export filtered results to CSV
python scripts/query_in_seekdb.py mobiles --get-all --where '{"Brand": {"$eq": "SAMSUNG"}}' --output samsung.csv

# Export hybrid search results with custom sheet name
python scripts/query_in_seekdb.py mobiles --hybrid --hybrid-query "gaming phone" --contains "64 GB" --output gaming.xlsx --sheet-name "Gaming Phones"
```

### Python API for Export

```python
from scripts.query_in_seekdb import query_by_text, results_to_dataframe, export_to_file

# Query data
results = query_by_text(
    collection_name="mobiles",
    query_text="phone with good camera",
    n_results=100
)

# Convert to DataFrame
df = results_to_dataframe(results, result_type="query")

# Export to file
export_to_file(df, "camera_phones.csv")
export_to_file(df, "camera_phones.xlsx", sheet_name="Phones")
```

### Supported Export Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| CSV | `.csv` | Comma-separated values, UTF-8 encoded with BOM |
| Excel | `.xlsx` | Excel workbook format |

## Filter Operators

### Metadata Filters (where)

| Operator | Description | Example |
|----------|-------------|---------|
| `$eq` | Equal to | `{"category": {"$eq": "AI"}}` |
| `$ne` | Not equal to | `{"status": {"$ne": "deleted"}}` |
| `$gt` | Greater than | `{"score": {"$gt": 90}}` |
| `$gte` | Greater than or equal | `{"score": {"$gte": 90}}` |
| `$lt` | Less than | `{"score": {"$lt": 50}}` |
| `$lte` | Less than or equal | `{"score": {"$lte": 50}}` |
| `$in` | In list | `{"tag": {"$in": ["ml", "ai"]}}` |
| `$nin` | Not in list | `{"tag": {"$nin": ["old"]}}` |
| `$or` | Logical OR | See below |
| `$and` | Logical AND | See below |

**Logical operators example:**

```python
where={
    "$or": [
        {"category": {"$eq": "AI"}},
        {"tag": {"$eq": "python"}}
    ]
}
```

### Document Filters (where_document)

| Operator | Description | Example |
|----------|-------------|---------|
| `$contains` | Contains substring | `{"$contains": "machine learning"}` |
| `$regex` | Regular expression | `{"$regex": "pattern.*"}` |

## CLI Examples

```bash
# Semantic search
python scripts/query_in_seekdb.py mobiles -q "phone with good battery" -n 5

# Search with metadata filter
python scripts/query_in_seekdb.py mobiles -q "budget phone" --where '{"Brand": {"$eq": "SAMSUNG"}}'

# Search with document filter
python scripts/query_in_seekdb.py mobiles -q "gaming phone" --contains "64 GB"

# Hybrid search
python scripts/query_in_seekdb.py mobiles --hybrid --hybrid-query "large screen phone" --contains "6.6 inch"

# Get all records
python scripts/query_in_seekdb.py mobiles --get-all --limit 20

# Get by IDs
python scripts/query_in_seekdb.py mobiles --get-ids "uuid1,uuid2"

# Collection info
python scripts/query_in_seekdb.py mobiles --info

# Output as JSON
python scripts/query_in_seekdb.py mobiles -q "smartphone" --json

# Export to CSV
python scripts/query_in_seekdb.py mobiles -q "smartphone" --output results.csv

# Export to Excel with custom sheet name
python scripts/query_in_seekdb.py mobiles --get-all --output data.xlsx --sheet-name "Mobile Data"
```

## Python API Examples

### Connect to seekdb

```python
import pyseekdb

# Embedded mode (local)
client = pyseekdb.Client()

# Server mode (remote)
# client = pyseekdb.Client(host="127.0.0.1", port=2881, database="test", user="root", password="")
```

### Query Imported Data

```python
# Get collection
collection = client.get_collection("mobiles")

# Semantic search
results = collection.query(
    query_texts="phone with good camera",
    n_results=5,
    include=["documents", "metadatas"]
)

# Print results
for i in range(len(results["ids"][0])):
    print(f"ID: {results['ids'][0][i]}")
    print(f"Distance: {results['distances'][0][i]:.4f}")
    print(f"Document: {results['documents'][0][i][:100]}...")
    print(f"Metadata: {results['metadatas'][0][i]}")
    print()
```

### Hybrid Search

```python
results = collection.hybrid_search(
    query={
        "where_document": {"$contains": "64 GB"},
        "n_results": 10
    },
    knn={
        "query_texts": ["smartphone with large battery"],
        "n_results": 10
    },
    rank={"rrf": {}},
    n_results=5,
    include=["documents", "metadatas"]
)
```

## User Interaction Guide

When user requests data query or export, ask:

1. **Collection name**: "Which collection do you want to query? (Use --list-collections to see available)"
2. **Query type**: "What type of query? (semantic search / hybrid search / get by ID / get all)"
3. **Search text**: "What are you looking for? (natural language query)"
4. **Filters**: "Any filters? (metadata or document content filters)"
5. **Result count**: "How many results do you need?"
6. **Export**: "Do you want to export the results? (CSV / Excel / terminal output)"

## Connection Configuration

Set environment variables for server mode:

| Variable | Description | Default |
|----------|-------------|---------|
| `SEEKDB_HOST` | Server host (if set, uses server mode) | - |
| `SEEKDB_PORT` | Server port | 2881 |
| `SEEKDB_DATABASE` | Database name | test |
| `SEEKDB_USER` | Username | root |
| `SEEKDB_PASSWORD` | Password | - |

## References

- [pyseekdb SDK Getting Started](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/10.pyseekdb-sdk-get-started.md)
- [query API](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/400.dql/200.query-interfaces-of-api.md)
- [get API](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/400.dql/300.get-interfaces-of-api.md)
- [hybrid_search API](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/400.dql/400.hybrid-search-of-api.md)
- [Filter Operators](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/400.dql/500.filter-operators-of-api.md)
