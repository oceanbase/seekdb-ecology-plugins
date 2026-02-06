# seekdb Documentation Examples

Complete workflow examples for common seekdb documentation queries.

## Example 1: Vector Search Query (Remote Access)

**User Query**: "How do I use vector search in seekdb?"

**Process**:

1. **Fetch remote catalog**
   ```
   URL: https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/450.reference/1600.seekdb-docs-catalog.md
   Result: Success → Mark conversation as "remote mode"
   ```

2. **Search catalog for matches**
   - Query: "vector search"
   - Found category: "Vector Search" under Development Guide
   - Matching entries:
     - Vector Search Introduction
     - Vector Similarity Search
     - Vector Index Basics

3. **Fetch relevant document**
   - File Path: `200.develop/100.vector-search/100.vector-search-overview/100.vector-search-intro.md`
   - Full URL: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/200.develop/100.vector-search/100.vector-search-overview/100.vector-search-intro.md`

4. **Read and extract answer**

---

## Example 2: Basic Overview Query (Local Fallback)

**User Query**: "What is seekdb?"

**Process**:

1. **Try remote catalog**
   ```
   URL: https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/450.reference/1600.seekdb-docs-catalog.md
   Result: Network error/timeout → Fallback to local
   ```

2. **Fetch local catalog**
   ```
   Path: /root/seekdb-docs/450.reference/1600.seekdb-docs-catalog.md
   Result: Success
   ```

3. **Search catalog for overview**
   - Query: "seekdb overview" or "what is seekdb"
   - Found entry under "Get Started" → "Overview"
   - Description: "An AI-native search database that unifies relational, vector, text, JSON, and GIS data..."

4. **Read local document**
   - File Path: `100.get-started/10.overview/10.seekdb-overview.md`
   - Local Path: `/root/seekdb-docs/100.get-started/10.overview/10.seekdb-overview.md`

5. **Provide answer based on local docs**

---

## Example 3: Multi-Turn Conversation (Remote Mode)

**First Query**:
- User: "How do I use vector search in seekdb?"
- Process: Remote catalog succeeds → "remote mode" enabled
- Answer: Provided from remote docs

**Second Query** (same conversation):
- User: "Now tell me about hybrid search"
- Process:
  1. Already in "remote mode" (from previous query)
  2. No need to re-fetch or re-check catalog source
  3. Search previously fetched catalog for "hybrid search"
  4. Found under "Hybrid Search" section
  5. File Path: `200.develop/200.hybrid-search/100.vector-index-hybrid-search.md`
  6. Fetch remote: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/200.develop/200.hybrid-search/100.vector-index-hybrid-search.md`
- Answer: Provided from remote docs

**Key**: Once remote succeeds, all subsequent queries in the same conversation use remote without re-checking.

---

## Example 4: Integration Query

**User Query**: "I want to integrate seekdb with jina"

**Process**:

1. **Fetch catalog** (remote first, local fallback)
   - Assume remote succeeds → "remote mode"

2. **Search catalog for integration matches**
   - Query keywords: "integrate", "jina"
   - Found category: "Model Platform Integrations"
   - Matching entry: "Guide to integrating seekdb vector search with Jina AI for embedding generation and semantic search..."
   - File Path: `300.integrations/200.model-platforms/100.jina.md`

3. **Fetch document**
   - Remote URL: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/300.integrations/200.model-platforms/100.jina.md`

4. **Extract integration steps and code examples**

---

## Example 5: SQL Syntax Query

**User Query**: "What's the syntax for creating a vector column?"

**Process**:

1. **Fetch catalog** (assume remote succeeds)

2. **Search for SQL/vector column syntax**
   - Query: "vector column", "CREATE TABLE", "SQL syntax"
   - Found under "Reference" → "SQL Syntax"
   - Multiple relevant entries:
     - Vector column definition syntax
     - CREATE TABLE statement
     - Data type reference

3. **Read relevant documents**
   - File Path: `450.reference/200.sql/100.sql-syntax/200.data-type/300.vector-type.md`
   - URL: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/450.reference/200.sql/100.sql-syntax/200.data-type/300.vector-type.md`

4. **Provide syntax with examples**

---

## Example 6: Deployment Guide Query

**User Query**: "How do I deploy seekdb in production?"

**Process**:

1. **Fetch catalog** (assume remote succeeds)

2. **Search deployment content**
   - Query: "deploy", "production", "installation"
   - Found under "Guides" → "Deployment"
   - Matching entries:
     - Production deployment guide
     - Docker deployment
     - Kubernetes deployment
     - Configuration best practices

3. **Read deployment documentation**
   - File Path: `400.guides/100.deployment/100.production-deployment.md`
   - URL: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/400.guides/100.deployment/100.production-deployment.md`

4. **Extract deployment steps and recommendations**

---

## Example 7: Error Code Lookup

**User Query**: "What does error code 4200 mean?"

**Process**:

1. **Fetch catalog** (assume remote succeeds)

2. **Search error code reference**
   - Query: "error code", "4200", "error codes"
   - Found under "Reference" → "Error Codes"
   - Entry: "Comprehensive list of seekdb error codes with descriptions and solutions"

3. **Read error code documentation**
   - File Path: `450.reference/400.error-code/100.error-code-list.md`
   - URL: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/450.reference/400.error-code/100.error-code-list.md`

4. **Locate error 4200 and provide explanation**

---

## Example 8: Tutorial Scenario

**User Query**: "Show me how to build a RAG app with seekdb"

**Process**:

1. **Fetch catalog** (assume remote succeeds)

2. **Search for RAG tutorial**
   - Query: "RAG", "retrieval augmented generation", "tutorial"
   - Found under "Tutorials" or "AI Coding"
   - Matching entry: "Building a RAG application using seekdb vector search and AI functions..."

3. **Read tutorial**
   - File Path: `500.tutorials/100.ai-applications/200.rag-tutorial.md`
   - URL: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/500.tutorials/100.ai-applications/200.rag-tutorial.md`

4. **Extract step-by-step tutorial with code examples**

---

## Example 9: SDK API Query

**User Query**: "What Python SDK methods does seekdb have?"

**Process**:

1. **Fetch catalog** (assume remote succeeds)

2. **Search SDK documentation**
   - Query: "SDK", "Python", "API", "client"
   - Found under "Reference" → "SDK APIs"
   - Entry: "Python SDK API reference with method signatures and examples"

3. **Read SDK reference**
   - File Path: `450.reference/500.sdk/100.python-sdk/100.api-reference.md`
   - URL: `https://raw.githubusercontent.com/davidzhangbj/seekdb-doc/V1.1.0/en-US/450.reference/500.sdk/100.python-sdk/100.api-reference.md`

4. **List available SDK methods with signatures**

---

## Key Patterns

1. **Always remote first**: Try remote catalog, fall back to local on failure
2. **Semantic matching**: Match by meaning, not just keywords
3. **Conversation state**: Maintain "remote mode" or "local mode" for consistency
4. **Multiple sources**: If multiple entries match, read all relevant docs
5. **Quick reference**: Check catalog's quick reference section for common topics
6. **Path construction**: Always append File Path to base URL/path from source mode
