---
name: seekdb-docs
description: Provides documentation and knowledge base for seekdb database. When users ask about SeekDB topics, automatically locate relevant documentation through index files.
---

# SeekDB Documentation Skill

This skill provides comprehensive documentation for the SeekDB database. When users ask about SeekDB-related topics, you should use the index files to locate and read the relevant documentation.

## How to Use This Skill

When a user asks about SeekDB, follow these steps:

### Step 1: Identify the Topic Category

Based on the user's query, determine which category index file to check:

- **Integration topics** (models, frameworks, MCP clients) → Check `integrations.md`
- **Development topics** (vector search, AI functions, SDK, APIs, multi-model data) → Check `develop.md`
- **Getting started topics** (overview, quick start, basic operations) → Check `get-started.md`
- **Operations topics** (deployment, OBShell, reference docs) → Check `guides.md`
- **Tutorial topics** → Check `tutorials.md`

### Step 2: Read the Appropriate Index File

Read the relevant index file to find matching documentation entries. Each index file contains:
- Category sections (marked with `###` or `####`)
- File entries with:
  - **File Path**: The path to the documentation file
  - **Description**: A brief description of what the document covers

### Step 3: Match the Query to Documentation

Search through the index file for entries whose **Description** matches the user's query. Look for:
- Exact keyword matches (e.g., "jina" → "Jina model integration")
- Related terms (e.g., "integration" → entries under "Model Integration", "Framework Integration", etc.)
- Category matches (e.g., "vector search" → entries under "Vector Search" section)

### Step 4: Read the Documentation File

Once you've identified the matching entry, read the file specified in the **File Path** field. The path is relative to the skill directory root.

## Examples

### Example 1: Integration Query
**User**: "I want to enhance the integration between SeekDB and jina"

**Process**:
1. Identify category: Integration → Check `integrations.md`
2. Read `integrations.md`
3. Find entry: Under "### Model Integration", locate "Jina model integration"
4. Extract file path: `official-docs/300.integrations/100.model/100.jina.md`
5. Read the file: `official-docs/300.integrations/100.model/100.jina.md`

### Example 2: Development Query
**User**: "How do I use vector search in SeekDB?"

**Process**:
1. Identify category: Development → Check `develop.md`
2. Read `develop.md`
3. Find entries: Under "### Vector Search", multiple relevant entries
4. Read relevant files: e.g., `official-docs/200.develop/100.vector-search/100.vector-search-overview/100.vector-search-intro.md`

### Example 3: Getting Started Query
**User**: "What is SeekDB?"

**Process**:
1. Identify category: Getting started → Check `get-started.md`
2. Read `get-started.md`
3. Find entry: "SeekDB Overview" section
4. Read file: `official-docs/100.get-started/10.overview/10.seekdb-overview.md`

## Guidelines

- **Always check index files first** before searching through the documentation directory
- **Read the full index file** to understand all available documentation in that category
- **Match descriptions semantically** - don't just look for exact keyword matches
- **If multiple entries match**, read all relevant files to provide comprehensive answers
- **If no exact match is found**, check related categories or suggest browsing the index file
- **File paths are relative** to the skill directory root (e.g., `official-docs/...`)

## Index Files Reference

- `integrations.md` - Integration guides for models, frameworks, and MCP clients
- `develop.md` - Development guides and technical documentation
- `get-started.md` - Quick start tutorials and basic operations
- `guides.md` - Deployment, operations, and reference documentation
- `tutorials.md` - Step-by-step tutorials

## Directory Structure

The `official-docs` directory contains all database documentation. Each file's name is the file's title. The directory is organized by topic categories with numbered prefixes for ordering.
