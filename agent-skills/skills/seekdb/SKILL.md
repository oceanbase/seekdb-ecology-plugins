---
name: seekdb-docs
description: seekdb database documentation lookup. Use when users ask about seekdb features, SQL syntax, vector search, hybrid search, integrations, deployment, or any seekdb-related topics. Automatically locates relevant docs via catalog-based semantic search.
---

# seekdb Documentation

Provides access to 1015 seekdb documentation entries through a catalog-based search system.

## Path Resolution (Do First)

All resource paths are relative to this SKILL.md's location. Resolve the skill directory first:

1. Read this SKILL.md to get its absolute path
2. Extract the parent directory as `<skill_dir>`
3. Catalog: `<skill_dir>references/seekdb-docs-catalog.jsonl`
4. Docs base: `<skill_dir>seekdb-docs/`

## Workflow

### Step 1: Search Catalog

**Grep search (preferred for ~90% of queries)**:
```bash
grep -i "keyword" <skill_dir>references/seekdb-docs-catalog.jsonl
```

**Full catalog load** (only when grep returns no results or semantic matching is needed):
- Local: `<skill_dir>references/seekdb-docs-catalog.jsonl`
- Remote fallback: `https://raw.githubusercontent.com/oceanbase/seekdb-ecology-plugins/main/agent-skills/skills/seekdb/references/seekdb-docs-catalog.jsonl`
- Format: JSONL — one `{"path": "...", "description": "..."}` per line (1015 entries)

### Step 2: Match Query

- Extract `path` and `description` from search results
- Select entries whose descriptions best match the query semantically (match by meaning, not just keywords)
- Consider multiple matches for comprehensive answers

### Step 3: Read Document

Local-first with remote fallback:
1. Try local: `<skill_dir>seekdb-docs/[path]`
2. Fallback: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.1.0/en-US/[path]`

## Example

```
Query: "How to integrate with Claude Code?"

1. grep -i "claude code" <skill_dir>references/seekdb-docs-catalog.jsonl
2. Match: {"path": "300.integrations/300.developer-tools/700.claude-code.md",
           "description": "This guide explains how to use the seekdb plugin with Claude Code..."}
3. Read: <skill_dir>seekdb-docs/300.integrations/300.developer-tools/700.claude-code.md
   Fallback: https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.1.0/en-US/300.integrations/300.developer-tools/700.claude-code.md
```

See [examples.md](references/examples.md) for more complete workflow examples.

## Notes

- **Optional local docs**: Run `scripts/update_docs.sh` to download full docs locally for offline/faster access
- **Offline capable**: With local docs and catalog present, works completely offline

## Category Overview

- **Get Started**: Quick start, basic operations, overview
- **Development**: Vector search, hybrid search, AI functions, MCP, multi-model
- **Integrations**: Frameworks, model platforms, developer tools, workflows
- **Guides**: Deployment, management, security, OBShell, performance
- **Reference**: SQL syntax, PL, error codes, SDK APIs
- **Tutorials**: Step-by-step scenarios
