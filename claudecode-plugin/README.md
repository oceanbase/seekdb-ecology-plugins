English | [简体中文](README_CN.md)  
# Seekdb Plugin for Claude Code

> This plugin contains seekdb skill for Claude Code that provides seekdb database-related documents.

## 📖 Project Overview

seekdb skill is designed specifically for Claude Code, aimed at enhancing Claude's capabilities in seekdb database scenarios. Through these Skills, Claude can query the complete seekdb official documentation and obtain technical guidance and best practices.

## ✨ Key Features

- **Complete Documentation Support**: Built-in seekdb official documentation knowledge base covering comprehensive technical documentation
- **Ready to Use**: Simple configuration to use in Claude Code

## 📦 Included Skills

### 1. seekdb-docs

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
- [SKILL.md](skills/seekdb-docs/SKILL.md)

## 🚀 Quick Start

### Prerequisites

- Claude Code 1.0 or higher
- Basic understanding of Agent Skills

### Installation

- Add seekdb's marketplace
```bash
/plugin marketplace add oceanbase/ecology-plugins
```
- Install plugins in Claude Code
```bash
/plugin install seekdb-plugin@seekdb
```

## 💡 Usage Examples

### Using seekdb-docs

Ask Claude seekdb-related technical questions:

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

Claude will automatically search the documentation library and provide accurate technical guidance.

## 📂 Project Structure

```
seekdb-claudecode-plugin/
├── README.md                           # Project documentation
├── README_CN.md                        # Chinese documentation
├── plugin.json                         # Plugin configuration
└── skills/
    └── seekdb-docs/                    # Document query skill
        ├── SKILL.md                    # Skill documentation
        ├── get-started.md              # Quick start documentation index
        ├── develop.md                  # Development guide documentation index
        ├── integrations.md             # Integration guide documentation index
        ├── guides.md                   # Operations guide documentation index
        ├── tutorials.md                # Practice tutorials documentation index
        └── official-docs/              # Official documentation library
            ├── 10.doc-overview.md      # Documentation overview
            ├── 100.get-started/        # Quick start guide
            ├── 200.develop/            # Development guide
            ├── 300.integrations/       # Integration guide
            ├── 400.guides/             # Operations guide
            └── 500.tutorials/          # Practice tutorials
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

- **Automatic Invocation**: Skills are automatically invoked by Claude based on context, no manual triggering required
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

A: Claude will automatically decide when to use them based on your request content and the Skills' descriptions. When you ask questions related to seekdb technical issues, the corresponding skill will be automatically invoked.

### Q: Can I use multiple Skills at the same time?

A: Yes. Claude can combine multiple Skills to complete complex tasks.

### Q: How to update Skills?

A: If managed with git, simply pull the latest code. If manually copied, you need to re-copy the updated files.

### Q: Will Skills affect Claude's other functionality?

A: No. Skills are independent modules that are only invoked when needed and will not affect Claude's other functionality.

---

**Happy Coding with seekdb and Claude! 🎉**

