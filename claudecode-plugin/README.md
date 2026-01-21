English | [简体中文](README_CN.md)  
# seekdb Plugin for Claude Code

> This plugin contains seekdb skill for Claude Code that provides seekdb database-related documents.

## 📖 Project Overview

seekdb skill is designed specifically for Claude Code, aimed at enhancing Claude's capabilities in seekdb database scenarios. Through these Skills, Claude Code can query the complete seekdb official documentation and obtain technical guidance and best practices.

## ✨ Key Features

- **Complete Documentation Support**: Built-in seekdb official documentation knowledge base covering comprehensive technical documentation
- **Ready to Use**: Simple configuration to use in Claude Code

## 📦 Included Skills

### 1. seekdb

Provides a complete seekdb database documentation knowledge base with document query and retrieval support.

**Features:**
- Covers complete seekdb official documentation
- Supports content-based semantic search
- Includes the following document categories:
  - Quick Start Guide
  - Development Guide (vector search, hybrid search, AI functions, etc.)
  - SDK and API Reference
  - Multi-model Data Support (JSON, spatial data, text, etc.)
  - Integration Guide (models, frameworks, MCP clients)
  - Deployment and Operations Guide
  - Practice Tutorials
  - Reference Documentation

**Related Documentation:**
- [SKILL.md](skills/seekdb/SKILL.md)

### 2. importing-to-seekdb

Import CSV or Excel files into seekdb vector database with optional column vectorization for semantic search.

**Features:**
- Read and preview Excel/CSV files before importing
- Import data to seekdb collections
- Automatic vectorization of specified columns using embedding functions (all-MiniLM-L6-v2, 384 dimensions)
- Batch processing for large files
- Collection management (create/delete)

**Related Documentation:**
- [SKILL.md](skills/importing-to-seekdb/SKILL.md)

### 3. querying-from-seekdb

Query and export data from seekdb vector database with support for scalar search, hybrid search, and export to CSV/Excel.

**Features:**
- Scalar search with metadata filtering
- Hybrid search combining fulltext and semantic search
- RRF (Reciprocal Rank Fusion) result ranking
- Export results to CSV or Excel format
- Collection information display

**Related Documentation:**
- [SKILL.md](skills/querying-from-seekdb/SKILL.md)

## 🚀 Quick Start

### Prerequisites

- Claude Code 1.0 or higher
- Basic understanding of Claude Skills
- Python 3.10+ (for importing-to-seekdb and querying-from-seekdb skills)
- Required Python packages (for data import/query skills):
  ```bash
  pip install pyseekdb pandas openpyxl
  ```

### Installing Claude Code

If you haven't installed Claude Code yet, install it using npm:

```bash
npm install -g @anthropic-ai/claude-code
```

### Configure Environment Variables

Claude Code requires an API key to run. Please set the following environment variables:

```bash
# Set API key (required)
export ANTHROPIC_API_KEY="your-api-key-here"

# Set API Base URL (if using a proxy or custom endpoint)
export ANTHROPIC_BASE_URL="https://api.anthropic.com"
```

> **Tip**: You can add these environment variables to your `~/.bashrc`, `~/.zshrc`, or other shell configuration files to persist the configuration.

### Configure seekdb Connection Mode

The `importing-to-seekdb` and `querying-from-seekdb` skills support two connection modes for seekdb:

**1. Embedded Mode (Default)**
- No additional configuration required
- Data is stored locally
- Simply run the scripts without setting any seekdb environment variables

**2. Server Mode**
- Connect to a remote seekdb server
- Configure the following environment variables:
  ```bash
  export SEEKDB_HOST=127.0.0.1
  export SEEKDB_PORT=2881
  export SEEKDB_USER=root
  export SEEKDB_PASSWORD=""
  export SEEKDB_DATABASE=test
  ```

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `SEEKDB_HOST` | Server host address (if set, enables server mode) | - |
| `SEEKDB_PORT` | Server port | 2881 |
| `SEEKDB_USER` | Username | root |
| `SEEKDB_PASSWORD` | Password | (empty) |
| `SEEKDB_DATABASE` | Database name | test |

> **Note**: If `SEEKDB_HOST` is not set, the scripts will automatically use embedded mode.

### Configure Network Settings

Since the seekdb skill plugin needs to fetch the latest documentation from GitHub, you need to configure Claude Code to allow network requests in your project directory.

Create or edit the `.claude/settings.local.json` file in your project root directory:

```json
{
  "skipWebFetchPreflight": true
}
```

> **Important Notes**:
> - Setting `skipWebFetchPreflight` to `true` skips the preflight check for network requests, allowing Claude to directly access remote documentation
> - If GitHub is not accessible, the plugin will automatically fall back to local documentation

### Installing the seekdb Plugin

Once Claude Code is installed, follow these steps to install the seekdb plugin:

1. **Add the seekdb Marketplace**
   
   Open Claude Code's terminal or command interface and run:
   ```bash
   /plugin marketplace add oceanbase/seekdb-ecology-plugins
   ```
   
   This command adds the seekdb plugin marketplace to your Claude Code instance.

2. **Install the Plugin**
   
   After adding the marketplace, install the seekdb plugin:
   ```bash
   /plugin install seekdb-plugin@seekdb
   ```
   
   This will download and install the seekdb plugin along with all its skills.

3. **Restart Claude Code**
   
   After installing the plugin, restart Claude Code to ensure the plugin is fully loaded and ready to use.

### Configuration

The plugin is ready to use immediately after installation. No additional configuration is required. The skills will be automatically available to Claude Code when you ask seekdb-related questions.

## 💡 Usage Examples

### Using seekdb-docs

Ask Claude Code seekdb-related technical questions:

```
How to deploy a seekdb test environment?
```

```
How to use seekdb's vector search functionality?
```

```
How to implement hybrid search in seekdb?
```

```
Which AI framework integrations does seekdb support?
```

Claude Code will automatically search the documentation library and provide accurate technical guidance.

### Using importing-to-seekdb

Import data files into seekdb with optional vectorization:

**Example 1: Preview Excel file before importing**
```
View the sample Excel data in the importing-to-seekdb skill
```

Claude Code will use `read_excel.py` to display the file structure and preview data:
```
File: sample_products.xlsx (11.5 KB)
Columns: Name, Brand, Selling Price, MRP, Discount, Ratings, No_of_ratings, Details
Records: 9 mobile phone products
```

**Example 2: Import Excel data with vectorization**
```
Import sample_products.xlsx into seekdb database, vectorize the Details column
```

Claude Code will:
1. Ask which column to vectorize (e.g., Details for semantic search)
2. Ask for collection name (default: derived from filename)
3. Execute the import with automatic embedding generation

```
Import Result:
- Collection: sample_products
- Records: 9
- Vectorized column: Details (all-MiniLM-L6-v2, 384 dimensions)
- Metadata fields: MRP, Name, Brand, Ratings, Discount, No_of_ratings, Selling Price
```

### Using querying-from-seekdb

Query data from seekdb with hybrid search and export capabilities:

**Example 1: Semantic search with metadata filtering**
```
Recommend 2 phones with rating above 4.3 and AMOLED screen
```

Claude Code will:
1. First run `--info` to understand the collection structure
2. Construct a query combining metadata filter (`Ratings >= 4.3`) and semantic search (`AMOLED screen`)
3. Return matching results ranked by relevance

```
Found 2 results:
1. POCO M4 Pro (Power Black 64 GB)
   - Brand: POCO
   - Rating: 4.3
   - Price: 10,999
   - Screen: 16.33 cm Full HD+ AMOLED Display

2. POCO M4 Pro (Power Black 128 GB)
   - Brand: POCO
   - Rating: 4.3
   - Price: 11,999
   - Screen: 16.33 cm Full HD+ AMOLED Display
```

**Example 2: Query and export to Excel**
```
Recommend 2 phones with rating above 4.3 and AMOLED screen, export to Excel
```

Claude Code will execute the search and export specified fields to an Excel file:
```
Exported 2 records to: amoled_phones.xlsx

| Name                             | Selling Price |
|----------------------------------|---------------|
| POCO M4 Pro (Power Black 64 GB)  | 10999         |
| POCO M4 Pro (Power Black 128 GB) | 11999         |
```

### Complete Workflow Example

Here's a complete workflow demonstrating all three skills together:

1. **Ask about seekdb** (seekdb skill):
   ```
   How to create a vector collection in seekdb?
   ```

2. **Import data** (importing-to-seekdb skill):
   ```
   Import the sample_products.xlsx file, vectorize the Details column
   ```

3. **Query and export** (querying-from-seekdb skill):
   ```
   Find all Samsung phones with rating >= 4.4, export to CSV
   ```

## 📖 Detailed Usage Guide

### Getting Started with Claude Code

1. **Open a New Conversation**
   - Launch Claude Code
   - Start a new conversation or open an existing project
   - The seekdb skills are automatically available in all conversations

2. **Ask seekdb Questions**
   - Simply type your question about seekdb in natural language
   - Claude Code will automatically detect when to use the seekdb-docs skill
   - No need to explicitly mention the skill name

3. **Example Interactions**

   **Basic Query:**
   ```
   How do I get started with seekdb?
   ```
   
   **Technical Question:**
   ```
   What are the best practices for vector search in seekdb?
   ```
   
   **Code Example Request:**
   ```
   Show me an example of implementing hybrid search with seekdb Python SDK
   ```

### Using Skills Effectively

- **Be Specific**: The more specific your question, the better Claude Code can search the documentation
- **Ask Follow-ups**: You can ask follow-up questions based on Claude Code's responses
- **Request Examples**: Ask for code examples, configuration samples, or step-by-step guides
- **Combine Topics**: Ask questions that combine multiple seekdb features

### Troubleshooting

If the skills don't seem to be working:

1. **Verify Plugin Installation**
   
   In Claude Code, run the `/plugin` command. This will open an interactive interface where you can browse and manage installed plugins.
   
   Select "Manage and uninstall plugins" to confirm that `seekdb-plugin` exists.

2. **Restart Claude Code**
   
   After installing new plugins or updates, you may need to restart Claude Code to load the updates.
   
   Completely close and reopen the Claude Code terminal session.

3. **Update the Plugin**
   
   You can update the plugin using either the interactive interface or command line:
   
   a. Open the plugin management interface:
      ```bash
      /plugin
      ```
   
   b. Navigate to "Manage marketplaces" using the arrow keys (↑↓) and press Enter to select.
   
   c. In the marketplace list, select the marketplace you want to update (e.g., `seekdb`).
   
   d. Press `u` to update the marketplace and its plugins.
   
   e. Press `Esc` to go back when finished.
   
   Make sure to use the correct plugin name and marketplace name format.

## 📂 Project Structure

```
claudecode-plugin/
├── README.md                           # Project documentation
├── README_CN.md                        # Chinese documentation
├── plugin.json                         # Plugin configuration
└── skills/
    ├── seekdb/                         # SeekDB documentation skill
    │   ├── SKILL.md                    # Skill documentation
    │   └── seekdb-docs/                # Official documentation library
    │       ├── 10.doc-overview.md      # Documentation overview
    │       ├── 100.get-started/        # Quick start guide
    │       ├── 200.develop/            # Development guide
    │       ├── 300.integrations/       # Integration guide
    │       ├── 400.guides/             # Operations guide
    │       ├── 450.reference/          # Reference documentation
    │       ├── 500.tutorials/          # Practice tutorials
    │       └── 600.demos/              # Demo projects
    │
    ├── importing-to-seekdb/            # Data import skill
    │   ├── SKILL.md                    # Skill documentation
    │   ├── scripts/
    │   │   ├── import_to_seekdb.py     # Main import script
    │   │   └── read_excel.py           # Excel preview script
    │   └── example-data/
    │       ├── sample_products.csv     # Sample CSV data
    │       └── sample_products.xlsx    # Sample Excel data
    │
    └── querying-from-seekdb/           # Data query skill
        ├── SKILL.md                    # Skill documentation
        └── scripts/
            └── query_from_seekdb.py    # Main query script
```

## 🔧 Development & Contribution

### Adding a New skill

To add a new skill for seekdb:

1. Create a new skill folder under the `./skills` directory
2. Add a `SKILL.md` file defining the skill's functionality and usage
3. Add necessary support files and example code
4. Update this README document

### Updating Documentation

The documentation content for seekdb-docs is located in the `./skills/seekdb-docs/official-docs` directory and can be synchronized based on updates to the seekdb official documentation.

## 📋 About Agent Skills

Agent Skills is a powerful feature of Claude Code that allows packaging professional knowledge and workflows into reusable modules:

- **Automatic Invocation**: Skills are automatically invoked by Claude Code based on context, no manual triggering required
- **Modular Design**: Each skill is independently maintained, making it easy to organize and manage
- **Team Sharing**: Share professional knowledge and workflows with your team through git
- **Composability**: Multiple Skills can be combined to solve complex tasks

Learn more about Agent Skills:
- [Agent Skills Overview](https://docs.anthropic.com/en/docs/agent-skills)
- [Using Agent Skills to Equip Agents for the Real World](https://www.anthropic.com/news/agent-skills)


## 🔗 Related Links

- [seekdb Official Website](https://www.oceanbase.ai/)
- [seekdb Official Documentation](https://www.oceanbase.ai/docs/)
- [Claude Code Documentation](https://www.claude.com/product/claude-code)

## ❓ Frequently Asked Questions

### Q: When will Skills be invoked?

A: Claude Code will automatically decide when to use them based on your request content and the Skills' descriptions. When you ask questions related to seekdb technical issues, the corresponding skill will be automatically invoked.

### Q: Can I use multiple Skills at the same time?

A: Yes. Claude Code can combine multiple Skills to complete complex tasks.

### Q: How to update Skills?

A: If managed with git, simply pull the latest code. If manually copied, you need to re-copy the updated files.

### Q: Will Skills affect Claude's other functionality?

A: No. Skills are independent modules that are only invoked when needed and will not affect Claude Code's other functionality.

