[English](README.md) | 简体中文
# Seekdb Claude Code 插件

> 本插件包含 seekdb 的 Claude Code 技能，提供 seekdb 数据库相关文档支持。

## 📖 项目概述

seekdb 技能为 Claude Code 设计，旨在增强 Claude 在 seekdb 数据库场景下的能力。通过这些技能，Claude 可以查询完整的 seekdb 官方文档，获取技术指导和最佳实践。

## ✨ 核心功能

- **完整文档支持**：内置 seekdb 官方文档知识库，涵盖全面的技术文档
- **开箱即用**：简单配置即可在 Claude Code 中使用

## 📦 包含的技能

### 1. seekdb-docs

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
- [SKILL.md](skills/seekdb-docs/SKILL.md)

## 🚀 快速开始

### 前置要求

- Claude Code 1.0 或更高版本
- 对 Agent Skills 的基本了解

### 安装

- 添加 seekdb 的市场
```bash
/plugin marketplace add oceanbase/seekdb-ecology-plugins
```
- 在 Claude Code 中安装插件
```bash
/plugin install seekdb-plugin@seekdb
```

## 💡 使用示例

### 使用 seekdb-docs

向 Claude 询问 seekdb 相关的技术问题：

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

Claude 会自动搜索文档库并提供准确的技术指导。

## 📂 项目结构

```
claudecode-plugin/
├── README.md                           # 项目文档
├── README_CN.md                        # 中文文档
├── plugin.json                         # 插件配置
└── skills/
    └── seekdb-docs/                    # 文档查询技能
        ├── SKILL.md                    # 技能文档
        ├── get-started.md              # 快速入门文档索引
        ├── develop.md                  # 开发指南文档索引
        ├── integrations.md             # 集成指南文档索引
        ├── guides.md                   # 运维指南文档索引
        ├── tutorials.md                # 实践教程文档索引
        └── official-docs/              # 官方文档库
            ├── 10.doc-overview.md      # 文档概览
            ├── 100.get-started/        # 快速入门
            ├── 200.develop/            # 开发指南
            ├── 300.integrations/       # 集成指南
            ├── 400.guides/             # 运维指南
            └── 500.tutorials/          # 实践教程
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

- **自动调用**：技能会根据上下文由 Claude 自动调用，无需手动触发
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

A: 不会。技能是独立的模块，只在需要时被调用，不会影响 Claude 的其他功能。

---

**祝您使用 seekdb 和 Claude Code 编码愉快！🎉**

