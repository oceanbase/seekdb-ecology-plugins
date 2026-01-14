English | [简体中文](claudecode-plugin_CN.md) 
# seekdb + Claude Code: Build an AI Programming Assistant with Vector Database Expertise

Claude Code, the AI programming assistant from Anthropic, is becoming an increasingly popular tool for developers thanks to its powerful code understanding and generation capabilities. However, when you ask Claude Code about seekdb-related questions, the AI may not provide accurate answers—because it has limited knowledge of seekdb, this emerging AI-native search database.

This article introduces how to use the seekdb Claude Code plugin to give Claude Code professional seekdb knowledge, enabling you to receive precise technical guidance during development.

## What is seekdb?

**seekdb** is an AI-native search database developed by OceanBase. It unifies relational data, vectors, text, JSON, and GIS data models within a single engine, supporting hybrid search and in-database AI workflows.

Typical use cases for seekdb include:
- RAG and Knowledge Retrieval: Introducing real-time, trusted external knowledge to large language models to improve response quality
- AI-Assisted Programming: Building vector and full-text indexes for code repositories to enable semantic-based code search
- Semantic Search Engines: Capturing user search intent for precise cross-modal retrieval
- Agent Applications: Providing a unified foundation for AI Agent memory, planning, perception, and reasoning

## What is the seekdb Claude Code Plugin?

The **seekdb Claude Code plugin** is an Agent Skill plugin that enables Claude Code to retrieve seekdb official documentation through Skill files, allowing it to understand seekdb database knowledge in context and:
- ✅ Understand seekdb database concepts: vector search, hybrid search, AI functions, etc.
- ✅ Provide accurate code suggestions: generate code following best practices based on official documentation
- ✅ Answer seekdb-related questions: get technical support directly in the terminal
- ✅ Accelerate development workflow: reduce time spent consulting documentation, focus on business logic

### Core Features
- 🚀 Two-command installation: Quick installation through the Claude Code plugin marketplace
- 📚 Complete documentation: Built-in seekdb official documentation knowledge base, covering comprehensive technical documentation on vector search, hybrid search, AI functions, and more
- 🌐 Dual-mode support: Prioritizes fetching latest documentation from GitHub, with local documentation as backup
- 🔄 Automatic invocation: Claude Code automatically uses seekdb skills based on questions, no manual triggering required

## Quick Start

### Prerequisites

Before installing the seekdb plugin, make sure you have Claude Code installed. If not, you can install it with the following command:

```bash  
npm install -g @anthropic-ai/claude-code  
```

Then configure your API key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"

# Set API Base URL (if using proxy or custom endpoint)
export ANTHROPIC_BASE_URL="https://api.anthropic.com"
```

### Step 1: Configure Network Settings

The seekdb skill plugin needs to fetch the latest documentation from GitHub, so you need to configure Claude Code to allow network requests.

Create or edit the `.claude/settings.local.json` file in your project root directory:

```bash
{
  "skipWebFetchPreflight": true
}
```

**Note**: Setting `skipWebFetchPreflight` to true skips the preflight check for network requests, allowing Claude to directly access remote documentation. If GitHub is inaccessible, the plugin will automatically fall back to local documentation.

### Step 2: Install the seekdb Plugin

Installation requires just two commands:

**1. Add the seekdb marketplace**

Run in Claude Code:

```bash
/plugin marketplace add oceanbase/seekdb-ecology-plugins
```

**2. Install the plugin**

```bash
/plugin install seekdb-plugin@seekdb
```

**3. Restart Claude Code**

After installation, exit and restart Claude Code to ensure the plugin loads correctly.

Now you can ask Claude Code any seekdb-related questions directly.

## Demo

Let's see how the seekdb Claude Code plugin helps you with development through a practical example.

### Example: Creating a seekdb Hybrid Search Application with Claude Code

After installing the plugin, start a new conversation in Claude Code and enter the following question:

> You: I want to create a simple seekdb application in Python that implements hybrid search for documents, please help me write the code

**Claude Code will provide an accurate response:**

```python
import pyseekdb

# ==================== Create Collection ====================
# Create embedded client
client = pyseekdb.Client(path="./seekdb.db")
# Create collection
collection = client.create_collection(
    name="hybrid_search_demo"
)

# ==================== Add Data ====================
# Define documents
documents = [
    "Machine learning is revolutionizing artificial intelligence and data science",
    "Python programming language is essential for machine learning developers",
    "Deep learning neural networks enable advanced AI applications",
    "Data science combines statistics, programming, and domain expertise",
    "Natural language processing uses machine learning to understand text",
    "Computer vision algorithms process images using deep learning techniques",
    "Reinforcement learning trains agents through reward-based feedback",
    "Python libraries like TensorFlow and PyTorch simplify machine learning",
    "Artificial intelligence systems can learn from large datasets",
    "Neural networks mimic the structure of biological brain connections"
]

# Define metadata
metadatas = [
    {"category": "AI", "topic": "machine learning", "year": 2023, "popularity": 95},
    {"category": "Programming", "topic": "python", "year": 2023, "popularity": 88},
    {"category": "AI", "topic": "deep learning", "year": 2024, "popularity": 92},
    {"category": "Data Science", "topic": "data analysis", "year": 2023, "popularity": 85},
    {"category": "AI", "topic": "nlp", "year": 2024, "popularity": 90},
    {"category": "AI", "topic": "computer vision", "year": 2023, "popularity": 87},
    {"category": "AI", "topic": "reinforcement learning", "year": 2024, "popularity": 89},
    {"category": "Programming", "topic": "python", "year": 2023, "popularity": 91},
    {"category": "AI", "topic": "general ai", "year": 2023, "popularity": 93},
    {"category": "AI", "topic": "neural networks", "year": 2024, "popularity": 94}
]

ids = [f"doc_{i+1}" for i in range(len(documents))]
# Insert data
collection.add(ids=ids, documents=documents, metadatas=metadatas)

# ==================== Execute Hybrid Search ====================
# Execute hybrid search
hybrid_result = collection.hybrid_search(
    query={"where_document": {"$contains": "machine learning"}, "n_results": 10},
    knn={"query_texts": ["AI research"], "n_results": 10},
    rank={"rrf": {}},
    n_results=5
)

# ==================== Print Query Results ====================
print("\nHybrid Search Results:")
print(f"  ids: {hybrid_result['ids'][0]}")
print(f"  Document: {hybrid_result['documents'][0]}")
```

### Running the Example

**1. Install pyseekdb**

```bash
pip install pyseekdb
```

**2. Create file and run**

Save the above code as `hybrid_search_demo.py`, then run:

```bash
python hybrid_search_demo.py
```

**3. View results**

```plaintext
Hybrid Search Results:
  ids: ['doc_1', 'doc_5', 'doc_2', 'doc_8', 'doc_3']
  Document: ['Machine learning is revolutionizing artificial intelligence and data science', 'Natural language processing uses machine learning to understand text', 'Python programming language is essential for machine learning developers', 'Python libraries like TensorFlow and PyTorch simplify machine learning', 'Deep learning neural networks enable advanced AI applications']
```

Hybrid search combines **keyword matching** (documents containing "machine learning") and **semantic search** (documents semantically similar to "AI research"), using the RRF (Reciprocal Rank Fusion) algorithm to merge the two retrieval results and return the most relevant documents.

## More Use Cases

After installing the seekdb Claude Code plugin, you can ask Claude Code various seekdb-related questions:

### Basic Queries

> How do I get started with seekdb?

> What deployment modes does seekdb support?

### Technical Questions

> How do I create a vector index in seekdb?

> What AI functions does seekdb have? How do I use the AI_EMBED function?

### Code Examples

> Show me an example of vector similarity search using seekdb SQL

> How do I integrate seekdb with LangChain?

### Integration Related

> How do I configure OpenAI models for vector embedding in seekdb?

## Plugin Management

### Verify Installation

Run the `/plugin` command in Claude Code. This will open an interactive interface where you can browse and manage installed plugins. Select "Manage and uninstall plugins" to confirm that `seekdb-plugin` exists.

### Update Plugin

1. Run `/plugin` to open the plugin management interface
2. Use arrow keys to navigate to "Manage marketplaces"
3. Select the `seekdb` marketplace
4. Press `u` to update the marketplace and its plugins

### Troubleshooting

If the skill doesn't seem to work properly:

1. **Verify plugin installation**: Run /plugin to confirm seekdb-plugin is installed
2. **Restart Claude Code**: Completely close and reopen the Claude Code terminal session
3. **Check network settings**: Ensure `skipWebFetchPreflight: true` is configured in `.claude/settings.local.json`

## How It Works

The seekdb Claude Code plugin is based on the Agent Skills feature:

1. Skill Injection: The plugin injects seekdb official documentation and skill description files into Claude Code
2. Automatic Invocation: When you ask seekdb-related questions, Claude Code automatically detects and uses the seekdb skill
3. Intelligent Retrieval: Claude Code precisely locates relevant documentation based on the document index and provides accurate answers

Compared to traditional manual documentation lookup, this approach allows you to get precise technical guidance anytime during programming without interrupting your workflow.

## About Agent Skills

Agent Skills allow packaging specialized knowledge and workflows into reusable modules:

- Automatic Invocation: Skills are automatically invoked by Claude based on context, no manual triggering required
- Modular Design: Each skill is independently maintained for easy organization and management
- Team Sharing: Share specialized knowledge and workflows with your team via git
- Composability: Multiple skills can be combined to solve complex tasks

Learn more about Agent Skills:
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Summary

With the **seekdb Claude Code plugin**, you can get seekdb official documentation support anytime while developing with Claude Code. Whether you're learning new seekdb features or solving technical problems during development, Claude Code can provide accurate guidance based on the latest official documentation.
