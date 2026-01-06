[English](README.md) | 简体中文
# seekdb Claude Code 插件

> 本插件包含 seekdb 的 Claude Code 技能，提供 seekdb 数据库相关文档支持。

## 📖 项目概述

seekdb 技能为 Claude Code 设计，旨在增强 Claude Code 在 seekdb 数据库场景下的能力。通过这些技能，Claude 可以查询完整的 seekdb 官方文档，获取技术指导和最佳实践。

## ✨ 核心功能

- **完整文档支持**：内置 seekdb 官方文档知识库，涵盖全面的技术文档
- **开箱即用**：简单配置即可在 Claude Code 中使用

## 📦 包含的技能

### 1. seekdb

提供完整的 seekdb 数据库文档知识库，支持文档查询和检索。

**功能特性：**
- 涵盖完整的 seekdb 官方文档
- 支持基于内容的语义搜索
- 包含以下文档类别：
  - 快速入门指南
  - 开发指南（向量搜索、混合搜索、AI 函数等）
  - SDK 和 API 参考
  - 多模型数据支持（JSON、空间数据、文本等）
  - 集成指南（模型、框架、MCP 客户端）
  - 部署和运维指南
  - 实践教程
  - 参考文档

**相关文档：**
- [SKILL.md](skills/seekdb/SKILL.md)

## 🚀 快速开始

### 前置要求

- Claude Code 1.0 或更高版本
- 对 Agent Skills 的基本了解

### 安装 Claude Code

如果你还没有安装 Claude Code，可以通过 npm 全局安装：

```bash
npm install -g @anthropic-ai/claude-code
```

### 配置环境变量

Claude Code 需要 API 密钥才能运行。请设置以下环境变量：

```bash
# 设置 API 密钥（必需）
export ANTHROPIC_API_KEY="your-api-key-here"

# 设置 API Base URL（如果使用代理或自定义端点）
export ANTHROPIC_BASE_URL="https://api.anthropic.com"
```

> **提示**：你可以将这些环境变量添加到 `~/.bashrc`、`~/.zshrc` 或其他 shell 配置文件中，以便持久化配置。

### 配置网络设置

由于 seekdb 技能插件需要从 GitHub 获取最新文档，你需要在项目目录下配置 Claude Code 允许网络请求。

在你的项目根目录下创建或编辑 `.claude/settings.local.json` 文件：

```json
{
  "skipWebFetchPreflight": true
}
```

> **重要说明**：
> - `skipWebFetchPreflight` 设置为 `true` 可跳过网络请求的预检，允许 Claude Code 直接访问远程文档
> - 如果无法访问 GitHub，插件会自动回退到本地文档

### 安装 seekdb 插件

1. **添加 seekdb 市场**

```bash
/plugin marketplace add oceanbase/seekdb-ecology-plugins
```

2. **安装插件**

```bash
/plugin install seekdb-plugin@seekdb
```

3. **重启 Claude Code**

安装完成后，需要重启 Claude Code 以确保插件正确加载。

## 💡 使用示例

### 使用 seekdb-docs

向 Claude Code 询问 seekdb 相关的技术问题：

```
如何部署 seekdb 测试环境？
```

```
如何使用 seekdb 的向量搜索功能？
```

```
如何在 seekdb 中实现混合搜索？
```

```
seekdb 支持哪些 AI 框架集成？
```

Claude Code 会自动搜索文档库并提供准确的技术指导。

## 📖 详细使用指南

### 开始使用 Claude Code

1. **打开新对话**
   - 启动 Claude Code
   - 开始新对话或打开现有项目
   - seekdb 技能在所有对话中自动可用

2. **询问 seekdb 问题**
   - 只需用自然语言输入关于 seekdb 的问题
   - Claude Code 会自动检测何时使用 seekdb 技能
   - 无需明确提及技能名称

3. **示例交互**

   **基础查询：**
   ```
   如何开始使用 seekdb？
   ```
   
   **技术问题：**
   ```
   seekdb 中向量搜索的最佳实践是什么？
   ```
   
   **代码示例请求：**
   ```
   展示一个使用 seekdb Python SDK 实现混合搜索的示例
   ```

### 有效使用技能

- **具体明确**：问题越具体，Claude 越能准确搜索文档
- **追问跟进**：可以根据 Claude Code 的回答提出后续问题
- **请求示例**：可以要求代码示例、配置示例或分步指南
- **组合主题**：可以提出结合多个 seekdb 功能的问题

### 故障排除

如果技能似乎无法正常工作：

1. **验证插件安装**
   
   在 Claude Code 中运行 `/plugin` 命令。这将打开一个交互式界面，您可以浏览和管理已安装的插件。
   
   选择"Manage and uninstall plugins"以确认 `seekdb-plugin` 存在。

2. **重启 Claude Code**
   
   安装新插件或更新后，您可能需要重启 Claude Code 以加载更新。
   
   完全关闭并重新打开 Claude Code 终端会话。

3. **更新插件**
   
   a. 打开插件管理界面：
      ```bash
      /plugin
      ```
   
   b. 使用方向键（↑↓）导航到"管理市场"，然后按 Enter 选择。
   
   c. 在市场列表中，选择要更新的市场（例如，`seekdb`）。
   
   d. 按 `u` 更新市场及其插件。
   
   e. 完成后按 `Esc` 返回。
   
   请确保使用正确的插件名称和市场名称格式。

## 📂 项目结构

```
claudecode-plugin/
├── README.md                           # 项目文档
├── README_CN.md                        # 中文文档
├── plugin.json                         # 插件配置
└── skills/
    └── seekdb/                         # SeekDB 技能
        ├── SKILL.md                    # 技能文档
        └── seekdb-docs/                # 官方文档库
            ├── 10.doc-overview.md      # 文档概览
            ├── 100.get-started/        # 快速入门
            ├── 200.develop/            # 开发指南
            ├── 300.integrations/       # 集成指南
            ├── 400.guides/             # 运维指南
            ├── 450.reference/          # 参考文档
            ├── 500.tutorials/          # 实践教程
            └── 600.demos/              # 演示项目
```

## 🔧 开发与贡献

### 添加新技能

要为 seekdb 添加新技能：

1. 在 `./skills` 目录下创建新的技能文件夹
2. 添加 `SKILL.md` 文件，定义技能的功能和使用方法
3. 添加必要的支持文件和示例代码
4. 更新本 README 文档

### 更新文档

seekdb-docs 的文档内容位于 `./skills/seekdb-docs/official-docs` 目录，可以根据 seekdb 官方文档的更新进行同步。

## 📋 关于 Agent Skills

Agent Skills 是 Claude Code 的强大功能，允许将专业知识和工作流程打包成可重用的模块：

- **自动调用**：技能会根据上下文由 Claude Code 自动调用，无需手动触发
- **模块化设计**：每个技能独立维护，便于组织和管理
- **团队共享**：通过 git 与团队共享专业知识和工作流程
- **可组合性**：多个技能可以组合使用来解决复杂任务

了解更多关于 Agent Skills：
- [Agent Skills 概述](https://docs.anthropic.com/en/docs/agent-skills)
- [使用 Agent Skills 为智能体配备真实世界能力](https://www.anthropic.com/news/agent-skills)

## 🔗 相关链接

- [seekdb 官方网站](https://www.oceanbase.ai/)
- [seekdb 官方文档](https://www.oceanbase.ai/docs/)
- [Claude Code 文档](https://www.claude.com/product/claude-code)

## ❓ 常见问题

### Q: 技能何时会被调用？

A: Claude Code 会根据您的请求内容和技能的描述自动决定何时使用它们。当您询问与 seekdb 技术相关的问题时，相应的技能会自动被调用。

### Q: 可以同时使用多个技能吗？

A: 可以。Claude Code 可以组合多个技能来完成复杂任务。

### Q: 如何更新技能？

A: 如果使用 git 管理，只需拉取最新代码。如果是手动复制，需要重新复制更新后的文件。

### Q: 技能会影响 Claude Code 的其他功能吗？

A: 不会。技能是独立的模块，只在需要时被调用，不会影响 Claude Code 的其他功能。

