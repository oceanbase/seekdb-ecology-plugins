---
name: importing-data-files
description: "Import CSV or Excel files into seekdb vector database. Supports automatic vectorization of specified columns using embedding functions. When users need to: (1) Import CSV/Excel data into seekdb, (2) Create vector collections from tabular data, (3) Vectorize specific text columns for semantic search, or (4) Batch insert product/document data with embeddings."
license: MIT
---

# Import Data Files to seekdb

Import CSV or Excel files into seekdb vector database with optional column vectorization for semantic search.

## Prerequisites

- Python 3.10+ installed
- Required packages:

```bash
pip install pyseekdb pandas openpyxl
```

## Quick Start

Use the provided `scripts/import_to_seekdb.py` script:

```bash
# Import with vectorization on Details column
python scripts/import_to_seekdb.py products.csv --vectorize-column Details

# Import without vectorization
python scripts/import_to_seekdb.py products.csv

# Import Excel with custom collection name
python scripts/import_to_seekdb.py products.xlsx -v Description -c my_products
```

## Scripts

This skill provides the following scripts in the `scripts/` directory:

| Script | Description |
|--------|-------------|
| `import_to_seekdb.py` | Main import script with CLI interface |
| `embedding_functions.py` | Custom embedding function classes |
| `data_utils.py` | Data reading and cleaning utilities |

## Workflow

### Step 1: Read Data File

Use `scripts/data_utils.py`:

```python
from scripts.data_utils import read_file, clean_dataframe

df = read_file('products.csv')  # or .xlsx
df = clean_dataframe(df)
print(f"Columns: {df.columns.tolist()}")
```

### Step 2: Connect to seekdb

```python
import pyseekdb

# Embedded mode (local)
client = pyseekdb.Client()

# Server mode (remote)
# client = pyseekdb.Client(host="127.0.0.1", port=2881, database="test", user="root", password="")
```

### Step 3: Create Collection

**With vectorization** (default embedding function):

```python
collection = client.get_or_create_collection(name="products")
```

**With custom embedding function** (see `scripts/embedding_functions.py`):

```python
from scripts.embedding_functions import OllamaEmbeddingFunction
from pyseekdb import HNSWConfiguration

ef = OllamaEmbeddingFunction(model="bge-m3")
config = HNSWConfiguration(dimension=ef.dimension, distance='cosine')
collection = client.get_or_create_collection(name="products", configuration=config, embedding_function=ef)
```

**Without vectorization**:

```python
from pyseekdb import HNSWConfiguration

config = HNSWConfiguration(dimension=384, distance='cosine')
collection = client.get_or_create_collection(name="products", configuration=config, embedding_function=None)
```

### Step 4: Import Data

```python
from scripts.data_utils import prepare_import_data

ids, documents, metadatas = prepare_import_data(df, vectorize_column='Details')

# With vectorization
collection.add(ids=ids, documents=documents, metadatas=metadatas)

# Without vectorization (must provide embeddings)
# collection.add(ids=ids, embeddings=your_embeddings, metadatas=metadatas)
```

### Step 5: Verify

```python
print(f"Total records: {collection.count()}")
preview = collection.peek(limit=3)
```

## User Interaction Guide

When user requests data import, ask:

1. **File path**: "Please provide the path to your CSV or Excel file."
2. **Vectorization**: "Would you like to enable vector search by vectorizing a column? (yes/no)"
3. **Column selection** (if yes): "Which column to vectorize? (e.g., 'Details', 'Description')"
4. **Collection name**: "Collection name? (default: derived from filename)"
5. **Connection mode**: "Embedded (local) or server mode?"

## Embedding Functions

Available in `scripts/embedding_functions.py`:

| Class | Model | Dimension | Requirements |
|-------|-------|-----------|--------------|
| `DefaultEmbeddingFunction` | all-MiniLM-L6-v2 | 384 | Built-in |
| `CustomEmbeddingFunction` | BAAI/bge-m3 | 1024 | sentence-transformers |
| `OllamaEmbeddingFunction` | bge-m3 | 1024 | Ollama |
| `RemoteEmbeddingFunction` | Any OpenAI-compatible | Configurable | requests |

## Handling Large Files

For files with >10,000 rows, the `import_to_seekdb.py` script uses batch processing automatically. You can configure batch size:

```bash
python scripts/import_to_seekdb.py large_file.csv -v Details --batch-size 500
```

## References

- [pyseekdb SDK Getting Started](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/10.pyseekdb-sdk-get-started.md)
- [create_collection API](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/200.collection/100.create-collection-of-api.md)
- [add API](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/300.dml/200.add-data-of-api.md)
