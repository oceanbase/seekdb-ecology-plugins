---
name: seekdb-docs
description: seekdb database documentation lookup. Use when users ask about seekdb features, SQL syntax, vector search, hybrid search, integrations, deployment, or any seekdb-related topics. Automatically locates relevant docs via catalog-based semantic search.
---

# seekdb Documentation

Provides comprehensive access to seekdb database documentation through a centralized catalog system.

## Quick Start

1. **Load full catalog** (951 documentation entries)
2. **Match query** to catalog entries semantically
3. **Read document** from matched entry

## Documentation Sources

### Full Catalog
- **Local**: `./seekdb-docs/450.reference/1600.seekdb-docs-catalog.md` (3969 lines, if local docs exist)
- **Remote**: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/450.reference/1600.seekdb-docs-catalog.md` (fallback)
- **Entries**: 951 documentation files
- **Coverage**: Complete seekdb documentation

### Complete Documentation (Local-First with Remote Fallback)

**Local Documentation** (if available):
- **Base Path**: `./seekdb-docs/`
- **Size**: 7.4M, 952 markdown files
- **Document Path**: Base Path + File Path

**Remote Documentation** (fallback):
- **Base URL**: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/`
- **Document URL**: Base URL + File Path

**Strategy**:
1. **Load**: Load full catalog (3969 lines) with all 951 documentation entries
2. **Search**: Semantic search through all catalog entries
3. **Read**: Try local `./seekdb-docs/` first, fallback to remote URL if missing

## Workflow

### Step 1: Load Full Catalog

Load the complete documentation catalog:
```
Local: ./seekdb-docs/450.reference/1600.seekdb-docs-catalog.md (if exists)
Remote: https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/450.reference/1600.seekdb-docs-catalog.md (fallback)
Size: 3969 lines
Entries: 951 documentation files
```

**Catalog contents**:
- All seekdb documentation organized by category
- Complete metadata: title, path, keywords, topics, summary, description
- Structured format for easy semantic matching

### Step 2: Match Query

Search the full catalog for semantic matches:
- **Search titles**: Match document titles
- **Match keywords**: Extracted keywords from each document
- **Match topics**: Category and topic labels
- **Match descriptions**: Detailed descriptions for context
- **Multiple results**: Return all relevant entries for comprehensive answers

### Step 3: Read Document

**Local-First Strategy**:

1. **Try local first**: `./seekdb-docs/[File Path]`
   - If file exists → read locally (fast)
   - If file missing → proceed to step 2

2. **Fallback to remote**: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/[File Path]`
   - Download from GitHub

**Example**:
```
Query: "How to integrate with Claude Code?"

Found in catalog → Claude Code entry:
- Path: 300.integrations/300.developer-tools/700.claude-code.md
- Keywords: claude, code, integration, mcp
- Topics: integration, developer-tools
- Summary: Instructions for integrating seekdb MCP Server with Claude Code
- Description: This guide explains how to install and use the seekdb plugin...

Try: ./seekdb-docs/300.integrations/300.developer-tools/700.claude-code.md
If not found: https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/300.integrations/300.developer-tools/700.claude-code.md
```

## Guidelines

- **Always use full catalog**: Load complete catalog for comprehensive search (951 entries)
- **Semantic matching**: Match by meaning, not just keywords
- **Multiple matches**: Read all relevant entries for comprehensive answers
- **Local-first with remote fallback**: Try local `./seekdb-docs/` first, use remote if missing
- **Optional local docs**: Run `scripts/update_docs.sh` to download full docs locally (faster)
- **Offline capable**: With local docs present, works completely offline

## Detailed Examples

See [examples.md](references/examples.md) for complete workflow examples including:
- Full catalog search scenarios
- Local-first lookup scenarios
- Remote fallback scenarios
- Integration queries
- Multi-turn conversations

## Category Overview

- **Get Started**: Quick start, basic operations, overview
- **Development**: Vector search, hybrid search, AI functions, MCP, multi-model
- **Integrations**: Frameworks, model platforms, developer tools, workflows
- **Guides**: Deployment, management, security, OBShell, performance
- **Reference**: SQL syntax, PL, error codes, SDK APIs
- **Tutorials**: Step-by-step scenarios
