---
name: seekdb-docs
description: Provides documentation and knowledge for seekdb database. When users ask about seekdb topics, automatically locate relevant documentation through the catalog file (remote-first with local fallback).
---

# seekdb Documentation Skill

This skill provides comprehensive documentation for the seekdb database. When users ask about seekdb-related topics, you should use the documentation catalog to locate and read the relevant documentation.

## Documentation Access Strategy

This skill supports both remote and local documentation access with the following priority:

### Remote-First, Local-Fallback

1. **First Attempt**: Try to access the remote documentation catalog
2. **Fallback**: If remote access fails, use the local documentation files
3. **Consistency**: Once remote access succeeds in a conversation, continue using remote files for that entire conversation

### Remote Documentation URLs

- **Base URL**: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/`
- **Catalog File**: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/450.reference/1600.seekdb-docs-catalog.md`
- **Full Document URL**: Base URL + File Path (from catalog)

### Local Documentation Paths

- **Catalog File**: `seekdb-docs/450.reference/1600.seekdb-docs-catalog.md`
- **Document Files**: `seekdb-docs/` + File Path (from catalog)

## How to Use This Skill

When a user asks about seekdb, follow these steps:

### Step 1: Access the Documentation Catalog

**Try Remote First:**
1. Fetch the remote catalog: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/450.reference/1600.seekdb-docs-catalog.md`
2. If successful, mark this conversation as "using remote docs"
3. If failed (network error, timeout, etc.), fall back to local catalog: `seekdb-docs/450.reference/1600.seekdb-docs-catalog.md`

The catalog contains:
- All documentation entries organized by category
- File paths for each documentation file
- Descriptions of what each document covers
- Quick reference section for common topics

### Step 2: Match the Query to Documentation

Search through the catalog for entries whose **Description** matches the user's query. Look for:
- Exact keyword matches (e.g., "jina" → "Jina model integration")
- Related terms (e.g., "integration" → entries under "Model Platform Integrations", "Framework Integrations", etc.)
- Category matches (e.g., "vector search" → entries under "Vector Search" section)

The catalog is organized into these main categories:
- **Get Started**: Quick start tutorials and basic operations
- **Development Guide**: Vector search, hybrid search, AI functions, MCP server, multi-model data
- **Integrations**: Frameworks, model platforms, developer tools, workflows, MCP clients
- **Guides**: Deployment, management, security, OBShell, performance testing
- **Reference**: SQL syntax, PL, error codes, SDK APIs
- **Tutorials**: Step-by-step tutorials and scenarios

### Step 3: Read the Documentation File

Once you've identified the matching entry, construct the full URL or path based on which source you're using:

**If using remote (preferred):**
- Full URL = `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/` + File Path
- Example: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/200.develop/100.vector-search/300.vector-similarity-search.md`

**If using local (fallback):**
- Local path = `seekdb-docs/` + File Path
- Example: `seekdb-docs/200.develop/100.vector-search/300.vector-similarity-search.md`

## Examples

### Example 1: Remote Access (Preferred)
**User**: "How do I use vector search in seekdb?"

**Process**:
1. Fetch remote catalog: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/450.reference/1600.seekdb-docs-catalog.md`
2. Remote access succeeds → mark conversation as "remote mode"
3. Find entries under "Vector Search" section
4. Fetch remote doc: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/200.develop/100.vector-search/100.vector-search-overview/100.vector-search-intro.md`

### Example 2: Local Fallback
**User**: "What is seekdb?"

**Process**:
1. Try to fetch remote catalog → fails (network error)
2. Fall back to local catalog: `seekdb-docs/450.reference/1600.seekdb-docs-catalog.md`
3. Find entry under "Seekdb Overview"
4. Read local file: `seekdb-docs/100.get-started/10.overview/10.seekdb-overview.md`

### Example 3: Subsequent Query in Same Conversation (Remote Mode)
**User**: "Now tell me about hybrid search"
(Previous query in this conversation successfully used remote)

**Process**:
1. Already in "remote mode" for this conversation
2. No need to re-check catalog source
3. Find entries under "Hybrid Search" section from previously fetched catalog
4. Fetch remote doc: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/200.develop/200.hybrid-search/100.vector-index-hybrid-search.md`

### Example 4: Integration Query
**User**: "I want to integrate seekdb with jina"

**Process**:
1. Access catalog (remote first, local fallback)
2. Find entry under "Model Platform Integrations": "Guide to integrating seekdb vector search with Jina AI..."
3. Extract file path: `300.integrations/200.model-platforms/100.jina.md`
4. Fetch/read the document using the appropriate source

## Guidelines

- **Always try remote first** before falling back to local files
- **Maintain consistency** within a conversation - if remote works, keep using remote
- **Match descriptions semantically** - don't just look for exact keyword matches
- **Use the Quick Reference section** at the bottom of the catalog for common topics
- **If multiple entries match**, read all relevant files to provide comprehensive answers

## URL Reference

### Remote (Primary)
- **Catalog**: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/450.reference/1600.seekdb-docs-catalog.md`
- **Base URL**: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/`

### Local (Fallback)
- **Catalog**: `seekdb-docs/450.reference/1600.seekdb-docs-catalog.md`
- **Base Path**: `seekdb-docs/`

## Directory Structure (Local)

The `seekdb-docs` directory contains all database documentation organized by topic categories:

```
seekdb-docs/
├── 100.get-started/     # Quick start and basic operations
├── 200.develop/         # Development guides (vector, hybrid, AI, multi-model)
├── 300.integrations/    # Framework, model, tool integrations
├── 400.guides/          # Deployment, management, security
├── 450.reference/       # SQL, PL, error codes, SDK reference
├── 500.tutorials/       # Step-by-step tutorials
└── 600.demos/           # Live demo information
```
