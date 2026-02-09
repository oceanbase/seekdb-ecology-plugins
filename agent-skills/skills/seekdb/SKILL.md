---
name: seekdb-docs
description: seekdb database documentation lookup. Use when users ask about seekdb features, SQL syntax, vector search, hybrid search, integrations, deployment, or any seekdb-related topics. Automatically locates relevant docs via catalog-based semantic search.
version: "V1.1.0"
---

# seekdb Documentation

Provides comprehensive access to seekdb database documentation through a centralized catalog system.

## Quick Start

1. **Locate skill directory** (see Path Resolution below)
2. **Load full catalog** (1015 documentation entries)
3. **Match query** to catalog entries semantically
4. **Read document** from matched entry

## Path Resolution (Critical First Step)

**Problem**: Relative paths like `./seekdb-docs/` are resolved from the **current working directory**, not from SKILL.md's location. This breaks when the agent's working directory differs from the skill directory.

**Solution**: Dynamically locate the skill directory before accessing docs.

### Step-by-Step Resolution

1. **Read SKILL.md itself** to get its absolute path:
   ```
   read(SKILL.md)  // or any known file in this skill directory
   ```

2. **Extract the directory** from the returned path:
   ```
   If read returns: /root/test-claudecode-url/.cursor/skills/seekdb/SKILL.md
   Skill directory =: /root/test-claudecode-url/.cursor/skills/seekdb/
   ```

3. **Construct paths** using this directory:
   ```
   Catalog path =: <skill directory>references/seekdb-docs-catalog.jsonl
   Docs base =: <skill directory>seekdb-docs/
   ```

**Why this works**: The `read` tool returns the absolute path, giving you a reliable anchor regardless of where the agent was invoked.

## Documentation Sources

### Full Catalog
- **Local**: `<skill directory>references/seekdb-docs-catalog.jsonl` (1015 entries, JSONL format)
- **Remote**: `https://raw.githubusercontent.com/oceanbase/seekdb-ecology-plugins/agent-skills/skills/seekdb/references/seekdb-docs-catalog.jsonl` (fallback)
- **Entries**: 1015 documentation files
- **Coverage**: Complete seekdb documentation
- **Format**: JSONL - one JSON object per line with path and description

### Complete Documentation (Local-First with Remote Fallback)

**Local Documentation** (if available):
- **Base Path**: `<skill directory>seekdb-docs/`
- **Size**: 7.4M, 952 markdown files
- **Document Path**: Base Path + File Path

**Remote Documentation** (fallback):
- **Base URL**: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.1.0/en-US/`
- **Document URL**: Base URL + File Path

**Strategy**:
1. **Locate**: Determine `<skill directory>` using path resolution above
2. **Load**: Load full catalog (1015 entries) - try local first, fallback to remote
3. **Search**: Semantic search through all catalog entries
4. **Read**: Try local docs first, fallback to remote URL if missing

## Workflow

### Step 0: Resolve Path (Do this first!)

```bash
# Read this file to discover its absolute path
read("SKILL.md")

# Extract directory from the path
# Example: /root/.claude/skills/seekdb/SKILL.md → /root/.claude/skills/seekdb/
```

### Step 1: Load Full Catalog

Load the complete documentation catalog:
```
Local: <skill directory>references/seekdb-docs-catalog.jsonl
Remote: https://raw.githubusercontent.com/oceanbase/seekdb-ecology-plugins/agent-skills/skills/seekdb/references/seekdb-docs-catalog.jsonl (fallback)
Format: JSONL (one JSON object per line)
Entries: 1015 documentation files
```

**Strategy**:
1. Try local catalog first: `<skill directory>references/seekdb-docs-catalog.jsonl`
2. If local missing, fetch from remote URL above

**Catalog contents**:
- Each line: {"path": "...", "description": "..."}
- All seekdb documentation indexed
- Optimized for semantic search and grep queries

### Step 2: Match Query

Search the full catalog for semantic matches:
- **Search descriptions**: Match against detailed document descriptions
- **Extract context**: Description contains topic and feature keywords
- **Multiple results**: Return all relevant entries for comprehensive answers

Note: The catalog contains `path` and `description` fields. Semantic matching is performed on the description text, which includes relevant keywords and context.

### Step 3: Read Document

**Local-First Strategy**:

1. **Try local first**: `<skill directory>seekdb-docs/[File Path]`
   - If file exists → read locally (fast)
   - If file missing → proceed to step 2

2. **Fallback to remote**: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.1.0/en-US/[File Path]`
   - Download from GitHub

**Example**:
```
Query: "How to integrate with Claude Code?"

1. Resolve path: read(SKILL.md) → /root/.claude/skills/seekdb/SKILL.md
   Skill directory =: /root/.claude/skills/seekdb/

2. Load catalog: /root/.claude/skills/seekdb/references/seekdb-docs-catalog.jsonl

3. Search catalog → Found Claude Code entry:
   {"path": "300.integrations/300.developer-tools/700.claude-code.md",
    "description": "This guide explains how to use the seekdb plugin with Claude Code..."}

4. Read doc:
   Try: /root/.claude/skills/seekdb/seekdb-docs/300.integrations/300.developer-tools/700.claude-code.md
   If missing: https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.1.0/en-US/300.integrations/300.developer-tools/700.claude-code.md
```

## Guidelines

- **Always resolve path first**: Use the read-your-SKILL.md trick to get the absolute path
- **Always use full catalog**: Load complete catalog for comprehensive search (1015 entries)
- **Semantic matching**: Match by meaning, not just keywords
- **Multiple matches**: Read all relevant entries for comprehensive answers
- **Local-first with remote fallback**: Try local docs first, use remote URL if missing
- **Optional local docs**: Run `scripts/update_docs.sh` to download full docs locally (faster)
- **Offline capable**: With local docs present, works completely offline

## Catalog Search Format

The catalog file is in **JSONL format** (one JSON object per line):

```json
{"path": "path/to/document.md", "description": "Document description text"}
```

**Searching the catalog**:

**Preferred method** - Read the full catalog:
- Read the entire catalog file
- Parse each line as JSON to extract path and description
- Perform semantic matching on description text

**Quick keyword search** - Use grep:
```bash
grep -i "keyword" references/seekdb-docs-catalog.jsonl
```
Each matched line contains both path and description together.

**Why JSONL is better**:
- ✅ One line per document - grep shows complete information
- ✅ Structured data - easy to parse with JSON tools
- ✅ No special flags needed - works naturally with grep, jq, etc.

## Common Installation Paths

This skill may be installed at:
- **Cursor**: `.cursor/skills/seekdb/`
- **Claude Code**: `.claude/skills/seekdb/`
- **Custom**: Any directory (path resolution handles this automatically)

**Do not hardcode these paths**. Use the dynamic resolution method instead.

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
