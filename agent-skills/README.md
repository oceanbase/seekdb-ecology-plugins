English | [简体中文](README_CN.md)  
# seekdb Agent Skills

> Contains seekdb Agent Skills, providing seekdb database documentation support and Excel/CSV import and export.

## 📖 Project Overview

This repository provides seekdb-related Agent Skills to enhance the capabilities of various AI assistants (e.g., Claude Code, OpenClaw) in seekdb database scenarios. Through documentation, import, and query skills, assistants can access seekdb official documentation, import Excel/CSV into seekdb, and perform scalar/hybrid search with result export.

## ✨ Key Features

- **Complete Documentation Support**: Built-in seekdb official documentation knowledge base covering comprehensive technical documentation
- **Ready to Use**: Simple configuration to use in supported AI tools

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

### Installation Methods

#### Method 1: Using PyPI Installer (Recommended for Multiple Tools)

This package can be installed from PyPI and provides an interactive command-line installer that supports multiple AI coding tools:

```bash
# Install from PyPI
pip install seekdb-agent-skills

# Run the interactive installer
seekdb-agent-skills
```

The interactive installer will guide you through the installation process:

1. **Project Root Confirmation**: The installer detects your current directory as the project root and asks for confirmation
2. **Tool Selection**: Choose one tool from the supported list (Claude Code, OpenClaw, Cursor, Codex, etc.)
3. **Skill Selection**: Select which skills to install (you can select multiple skills using Space key)
4. **Automatic Installation**: The installer automatically copies the selected skills to the correct directories for your chosen tool

**Supported Tools:**
- Claude Code (`.claude/skills`)
- OpenClaw (`~/.openclaw/workspace/skills`)
- Cursor (`.cursor/skills`)
- Codex (`.agents/skills`)
- OpenCode (`.opencode/skills`)
- GitHub Copilot (`.github/skills`)
- Qoder (`.qoder/skills`)
- Trae (`.trae/skills`)

**Interactive Features:**
- Navigate with arrow keys (↑↓)
- Select multiple skills with Space key
- Confirm with Enter
- Cancel anytime with Ctrl+C

#### Method 2: Through Marketplace (Claude Code)

Install with just two commands:

1. **Add the seekdb marketplace**  
   In Claude Code, run:  
   `/plugin marketplace add oceanbase/seekdb-ecology-plugins`

2. **Install the plugin**  
   `/plugin install seekdb-plugin@seekdb`

3. **Restart Claude Code**  
   After installation, exit and restart Claude Code to ensure the plugin loads correctly.

### Prerequisites

- **Python 3.10+**: Required for the installer and when using the data import/query skills
- **Basic understanding of Agent Skills**: When using an AI coding tool that supports skills/plugins
- **Data import/query skills** also require the following Python packages:
  ```bash
  pip install pyseekdb pandas openpyxl
  ```

### Installing Claude Code

If you haven't installed Claude Code yet, install it globally with npm:

```bash
npm install -g @anthropic-ai/claude-code
```

For other AI coding tools, please refer to their respective official documentation.

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

┌─────┬──────────────────────────────────┬───────┬─────────┬─────────┬──────────┐
│  #  │               Name               │ Brand │ Ratings │  Price  │ Discount │
├─────┼──────────────────────────────────┼───────┼─────────┼─────────┼──────────┤
│ 1   │ POCO M4 Pro (Power Black 64 GB)  │ POCO  │   4.3   │ ₹10,999 │  38% off │
├─────┼──────────────────────────────────┼───────┼─────────┼─────────┼──────────┤
│ 2   │ POCO M4 Pro (Power Black 128 GB) │ POCO  │   4.3   │ ₹11,999 │  40% off │
└─────┴──────────────────────────────────┴───────┴─────────┴─────────┴──────────┘
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
agent-skills/
├── README.md                           # Project documentation
├── README_CN.md                        # Chinese documentation
├── plugin.json                         # Plugin configuration
├── pyproject.toml                      # Python package configuration
├── MANIFEST.in                         # Package data manifest
├── upload_to_pypi.py                   # Build and package script
├── .gitignore                          # Git ignore rules
├── skills/                             # Skills directory (source)
│   ├── seekdb/                         # SeekDB documentation skill
│   │   ├── SKILL.md                    # Skill documentation
│   │   ├── references/                 # Quick index and metadata
│   │   │   ├── quick-index.md          # Quick search index (383 lines)
│   │   │   ├── examples.md             # Usage examples
│   │   │   └── catalog-index.json      # JSON catalog
│   │   ├── scripts/                    # Utility scripts
│   │   │   └── update_docs.sh          # Update documentation from GitHub
│   │   └── seekdb-docs/                # Official documentation library (local-first)
│   │       ├── 10.doc-overview.md      # Documentation overview
│   │       ├── 100.get-started/        # Quick start guide
│   │       ├── 200.develop/            # Development guide
│   │       ├── 300.integrations/       # Integration guide
│   │       ├── 400.guides/             # Operations guide
│   │       ├── 450.reference/          # Reference documentation
│   │       ├── 500.tutorials/          # Practice tutorials
│   │       └── 600.demos/              # Demo projects
│   │
│   ├── importing-to-seekdb/            # Data import skill
│   │   ├── SKILL.md                    # Skill documentation
│   │   ├── scripts/
│   │   │   ├── import_to_seekdb.py     # Main import script
│   │   │   └── read_excel.py           # Excel preview script
│   │   └── example-data/
│   │       ├── sample_products.csv     # Sample CSV data
│   │       └── sample_products.xlsx    # Sample Excel data
│   │
│   └── querying-from-seekdb/           # Data query skill
│       ├── SKILL.md                    # Skill documentation
│       └── scripts/
│           └── query_from_seekdb.py    # Main query script
│
└── src/                                # Python package source
    └── seekdb_plugin_installer/        # Package directory
        ├── __init__.py
        ├── main.py                     # CLI entry point (interactive installer)
        └── skills/                     # Skills (synced during build)
            └── ...                     # Same structure as root skills/
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

### Building and Publishing to PyPI

This project is packaged as a Python package and can be published to PyPI for easy distribution.

**Package Configuration:**
- Package name: `seekdb-agent-skills`
- Entry point: `seekdb-agent-skills` command (defined in `pyproject.toml`)
- Dependencies: `questionary>=1.10.0` (for interactive CLI)

**Building the Package:**

Use the provided build script to package the project:

```bash
# Run the build script (syncs skills, builds wheel, cleans up)
python upload_to_pypi.py
```

This script will:
1. Sync the `skills/` directory to `src/seekdb_plugin_installer/skills/`
2. Build the wheel package using `python -m build`
3. Clean up by removing the skills from the package directory
4. Output the built artifacts in the `dist/` directory

**Manual Build Steps:**

If you prefer to build manually:

```bash
# 1. Sync skills to package directory
cp -r skills src/seekdb_plugin_installer/

# 2. Build the package
python -m build

# 3. Clean up (optional)
rm -rf src/seekdb_plugin_installer/skills
```

**Publishing to PyPI:**

After building, you can upload to PyPI:

```bash
# Upload to PyPI (requires authentication)
python -m twine upload dist/*
```

**Note:** Make sure to update the version number in `pyproject.toml` before publishing a new release.

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

