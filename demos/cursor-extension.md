English | [简体中文](cursor-extension_CN.md) 
# Make Cursor AI Assistant Understand seekdb: seekdb Cursor Extension User Guide

In the era of AI-assisted programming, developers increasingly rely on intelligent tools to boost coding efficiency. However, when you ask Cursor about seekdb-related questions, the AI may not provide accurate answers—because it doesn't know about seekdb, this emerging AI-native search database.

This article introduces how to use the **seekdb Cursor Extension** to give the Cursor AI assistant professional seekdb knowledge, enabling you to receive precise technical guidance during development.

## What is seekdb?

**seekdb** is an AI-native search database developed by OceanBase. It unifies relational data, vectors, text, JSON, and GIS data models within a single engine, supporting hybrid search and in-database AI workflows.

Typical use cases for seekdb include:
- **RAG and Knowledge Retrieval**: Introducing real-time, trusted external knowledge to large language models to improve response quality
- **AI-Assisted Programming**: Building vector and full-text indexes for code repositories to enable semantic-based code search
- **Semantic Search Engines**: Capturing user search intent for precise cross-modal retrieval
- **Agent Applications**: Providing a unified foundation for AI Agent memory, planning, perception, and reasoning

## What is seekdb Cursor Extension?

**seekdb Cursor Extension** is a Cursor extension that adds rules to the `.cursor/rules` directory, enabling the Cursor AI assistant to retrieve seekdb official documentation and understand seekdb database knowledge, allowing it to:
- ✅ Understand seekdb database concepts: vector search, hybrid search, AI functions, etc.
- ✅ Provide accurate code suggestions: generate code following best practices based on official documentation
- ✅ Answer seekdb-related questions: get technical support directly in the editor
- ✅ Accelerate development workflow: reduce time spent consulting documentation, focus on business logic

### Core Features
- 🚀 **One-click installation**: Quick installation through Cursor extension marketplace or command palette
- 📚 **Complete documentation**: Retrieve seekdb official documentation knowledge base, covering comprehensive technical documentation on vector search, hybrid search, AI functions, and more
- 🌐 **Dual-mode support**: Prioritizes fetching latest documentation from GitHub, with local documentation as backup

## Quick Start

### Step 1: Install the Extension

1. Open the extension marketplace in Cursor (`Ctrl+Shift+X` or `Cmd+Shift+X`)
2. Search for "seekdb"
3. Click **Install** to install the extension

### Step 2: Add seekdb Documentation

1. Open a project directory in Cursor (documentation will be added to this directory)
2. Open the command palette:
    - Windows/Linux: Press `Ctrl+Shift+P`
    - macOS: Press `Cmd+Shift+P`
3. Enter and select the command:
    - Type "**seekdb**" or "**Add seekdb Docs**"
    - Select the `Add seekdb Docs` command
4. Documentation will be added automatically:
    - `.cursor/rules/seekdb-docs` directory (official documentation)
    - `.cursor/rules/seekdb.mdc` file (rules file)
5. Reload the window for the rules to take effect

Installation complete! Now you can ask the Cursor AI assistant any seekdb-related questions directly.

## Demo

Let's see how the seekdb Cursor Extension helps you with development through a practical example.

### Example: Creating a seekdb Hybrid Search Application with AI Assistant

After installing the extension and adding documentation, start a new conversation in Cursor and enter the following question:

> You: I want to create a simple seekdb application in Python that implements hybrid search for documents, please help me write the code

**Cursor AI assistant will provide an accurate response**:

```python
"""
seekdb Hybrid Search Quick Start Example

This is a minimal hybrid search example to help you get started quickly.
"""

import pyseekdb

# 1. Create client (embedded mode, no database deployment required)
client = pyseekdb.Client()

# 2. Create collection
collection = client.get_or_create_collection(name="my_docs")

# 3. Add documents
documents = [
    "Machine learning is the core technology of artificial intelligence",
    "Python is the most popular programming language for machine learning",
    "Deep learning requires large amounts of training data",
    "Natural language processing enables computers to understand human language",
    "Vector databases are used to store and retrieve vector data",
]

metadatas = [
    {"category": "AI", "year": 2024},
    {"category": "Programming", "year": 2024},
    {"category": "AI", "year": 2023},
    {"category": "AI", "year": 2024},
    {"category": "Database", "year": 2024},
]

ids = [f"doc_{i}" for i in range(len(documents))]

collection.add(ids=ids, documents=documents, metadatas=metadatas)
print(f"✅ Added {len(documents)} documents")

# 4. Execute hybrid search
# Combine full-text search (containing "machine learning") and vector semantic search (find content similar to "AI technology")
results = collection.hybrid_search(
    query={
        "where_document": {"$contains": "machine learning"},  # Full-text search: contains keyword
        "n_results": 10,
    },
    knn={
        "query_texts": ["AI technology"],  # Vector search: semantic similarity
        "n_results": 10,
    },
    rank={"rrf": {}},  # Use RRF algorithm to fuse results
    n_results=3,
    include=["documents", "metadatas"],
)

# 5. Print results
print("\n🔍 Hybrid Search Results:")
for i, (doc_id, doc, meta) in enumerate(
    zip(results["ids"][0], results["documents"][0], results["metadatas"][0]), 1
):
    print(f"  [{i}] {doc}")
    print(f"      Metadata: {meta}\n")

# 6. Cleanup (optional)
# client.delete_collection("my_docs")
```

### Running the Example

1. **Install pyseekdb**

```bash
pip install pyseekdb
```

2. **Run the code**

```bash
python quick_start_hybrid_search.py
```

3. **View results**

```bash
✅ Added 5 documents

🔍 Hybrid Search Results:
  [1] Machine learning is the core technology of artificial intelligence
      Metadata: {'year': 2024, 'category': 'AI'}

  [2] Deep learning requires large amounts of training data
      Metadata: {'year': 2023, 'category': 'AI'}

  [3] Python is the most popular programming language for machine learning
      Metadata: {'year': 2024, 'category': 'Programming'}
```

Hybrid search combines **keyword matching** (documents containing "machine learning") and **semantic search** (documents semantically similar to "AI technology"), using the RRF (Reciprocal Rank Fusion) algorithm to merge the two retrieval results and return the most relevant documents.

## More Use Cases

After installing the seekdb Cursor Extension, you can ask the AI assistant various seekdb-related questions:

### Basic Queries

```plaintext
How do I get started with seekdb?
```

```plaintext
What deployment modes does seekdb support?
```

### Technical Questions

```plaintext
How do I create a vector index in seekdb?
```

```plaintext
What AI functions does seekdb have? How do I use the AI_EMBED function?
```

### Code Examples

```plaintext
Show me an example of vector similarity search using seekdb SQL
```

```plaintext
How do I integrate seekdb with LangChain?
```

### Integration Related

```plaintext
How do I configure OpenAI models for vector embedding in seekdb?
```

## How It Works

The seekdb Cursor Extension works in a straightforward way:

1. **Rule File Injection**: The extension adds seekdb official documentation and .mdc rule files to the .cursor/rules directory
2. **AI Context Enhancement**: Cursor automatically reads the contents of the .cursor/rules directory as context knowledge for the AI assistant
3. **Intelligent Retrieval**: When you ask seekdb-related questions, the AI assistant provides accurate answers based on this documentation

## Remove Documentation

If you no longer need the seekdb documentation, you can easily remove it:

1. Open the command palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Type "**Remove seekdb Docs**"
3. Select and execute the command

The documentation will be removed from the `.cursor/rules` directory.

## Summary

With the **seekdb Cursor Extension**, you can get seekdb official documentation support anytime while developing with Cursor. Whether you're learning new seekdb features or solving technical problems during development, the AI assistant can provide accurate guidance based on the latest official documentation.
