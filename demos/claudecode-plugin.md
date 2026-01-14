# seekdb + Claude Code：打造懂向量数据库的 AI 编程助手
Claude Code 作为 Anthropic 推出的 AI 编程助手，凭借强大的代码理解和生成能力，正在成为越来越多开发者的得力工具。然而，当你在 Claude Code 中询问 seekdb 相关问题时，AI 可能无法给出准确的回答——因为它对 seekdb 这款新兴的 AI 原生搜索数据库了解有限。  
本文将介绍如何通过 seekdb Claude Code 插件，让 Claude Code 拥有 seekdb 专业知识，从而在开发过程中获得精准的技术指导。
## 什么是 seekdb？
**seekdb** 是由 OceanBase 推出的一款 AI 原生搜索数据库。它在单一引擎中统一了关系型数据、向量、文本、JSON 和 GIS 等多种数据模型，支持混合搜索和数据库内的 AI 工作流。  
seekdb 的典型应用场景包括：  
- RAG 与知识检索：为大语言模型引入实时可信的外部知识，提升回答质量
- AI 辅助编程：为代码仓库构建向量和全文索引，实现基于语义的代码搜索
- 语义搜索引擎：捕捉用户搜索意图，实现跨模态精准检索
- 智能体（Agent）应用：为 AI Agent 提供记忆、规划、感知和推理的统一基础
## 什么是 seekdb Claude Code 插件？
**seekdb Claude Code** 插件 是一款 Agent Skill 插件，通过 Skill 文件使 Claude Code 可以检索 seekdb 官方文档，从而理解 seekdb 数据库知识的上下文中，使其能够：  
- ✅ 理解 seekdb 数据库概念：向量搜索、混合搜索、AI 函数等
- ✅ 提供准确的代码建议：基于官方文档生成符合最佳实践的代码
- ✅ 回答 seekdb 相关问题：直接在终端中获取技术支持
- ✅ 加速开发流程：减少查阅文档的时间，专注于业务逻辑
### 核心特性
- 🚀 两条命令安装：通过 Claude Code 插件市场快速安装
- 📚 完整文档：内置 seekdb 官方文档知识库，涵盖向量搜索、混合搜索、AI 函数等全面技术文档
- 🌐 双模式支持：优先从 GitHub 获取最新文档，本地文档作为备份
- 🔄 自动调用：Claude Code 会根据问题自动使用 seekdb 技能，无需手动触发
## 快速开始
### 前置要求
在安装 seekdb 插件之前，请确保你已经安装了 Claude Code。如果还未安装，可以通过以下命令安装：
```bash  
npm install -g @anthropic-ai/claude-code  
```
然后配置你的 API 密钥：  
```bash
export ANTHROPIC_API_KEY="your-api-key-here"

# 设置 API Base URL（如果使用代理或自定义端点）
export ANTHROPIC_BASE_URL="https://api.anthropic.com"
```
### 第一步：配置网络设置
seekdb 技能插件需要从 GitHub 获取最新文档，因此需要配置 Claude Code 允许网络请求。  
在你的项目根目录下创建或编辑 .claude/settings.local.json 文件：  
```bash
{
  "skipWebFetchPreflight": true
}
```
**说明**：`skipWebFetchPreflight` 设置为 true 可跳过网络请求的预检，允许 Claude 直接访问远程文档。如果无法访问 GitHub，插件会自动回退到本地文档。
### 第二步：安装 seekdb 插件
只需两条命令即可完成安装：  
**1. 添加 seekdb 市场**  
在 Claude Code 中运行：
```bash
/plugin marketplace add oceanbase/seekdb-ecology-plugins
```
**2. 安装插件**
```bash
/plugin install seekdb-plugin@seekdb
```
**3. 重启 Claude Code**  
安装完成后，退出并重新启动 Claude Code 以确保插件正确加载。  
现在你可以直接向 Claude Code 询问任何 seekdb 相关问题了。  
## 实际效果演示
让我们通过一个实际示例，看看 seekdb Claude Code 插件如何帮助你进行开发。  
### 示例：使用 Claude Code 创建一个 seekdb 混合搜索应用
安装插件后，在 Claude Code 中开始一个新对话，输入以下问题：  
> 你：我想用 Python 创建一个简单的 seekdb 应用，实现文档的混合搜索功能，请帮我写代码

**Claude Code 会给出准确的回答：**
```python
import pyseekdb

# ==================== 创建集合 ====================
# 创建嵌入式客户端
client = pyseekdb.Client(path="./seekdb.db")
# 创建集合
collection = client.create_collection(
    name="hybrid_search_demo"
)

# ==================== 添加数据 ====================
# 定义文档
documents = [
    "Machine learning is revolutionizing artificial intelligence and data science",
    "Python programming language is essential for machine learning developers",
    "Deep learning neural networks enable advanced AI applications",
    "Data science combines statistics, programming, and domain expertise",
    "Natural language processing uses machine learning to understand text",
    "Computer vision algorithms process images using deep learning techniques",
    "Reinforcement learning trains agents through reward-based feedback",
    "Python libraries like TensorFlow and PyTorch simplify machine learning",
    "Artificial intelligence systems can learn from large datasets",
    "Neural networks mimic the structure of biological brain connections"
]

# 定义元数据
metadatas = [
    {"category": "AI", "topic": "machine learning", "year": 2023, "popularity": 95},
    {"category": "Programming", "topic": "python", "year": 2023, "popularity": 88},
    {"category": "AI", "topic": "deep learning", "year": 2024, "popularity": 92},
    {"category": "Data Science", "topic": "data analysis", "year": 2023, "popularity": 85},
    {"category": "AI", "topic": "nlp", "year": 2024, "popularity": 90},
    {"category": "AI", "topic": "computer vision", "year": 2023, "popularity": 87},
    {"category": "AI", "topic": "reinforcement learning", "year": 2024, "popularity": 89},
    {"category": "Programming", "topic": "python", "year": 2023, "popularity": 91},
    {"category": "AI", "topic": "general ai", "year": 2023, "popularity": 93},
    {"category": "AI", "topic": "neural networks", "year": 2024, "popularity": 94}
]

ids = [f"doc_{i+1}" for i in range(len(documents))]
# 插入数据
collection.add(ids=ids, documents=documents, metadatas=metadatas)

# ==================== 执行混合搜索 ====================
# 执行混合搜索
hybrid_result = collection.hybrid_search(
    query={"where_document": {"$contains": "machine learning"}, "n_results": 10},
    knn={"query_texts": ["AI research"], "n_results": 10},
    rank={"rrf": {}},
    n_results=5
)

# ==================== 打印查询结果 ====================
print("\n混合搜索结果:")
print(f"  ids: {hybrid_result['ids'][0]}")
print(f"  Document: {hybrid_result['documents'][0]}")
```
### 运行示例
**1. 安装 pyseekdb**
```bash
pip install pyseekdb
```
**2. 创建文件并运行**
将上述代码保存为 `hybrid_search_demo.py`，然后运行：  
```bash
python hybrid_search_demo.py
```
**3. 查看结果**
```plaintext
混合搜索结果:
  ids: ['doc_1', 'doc_5', 'doc_2', 'doc_8', 'doc_3']
  Document: ['Machine learning is revolutionizing artificial intelligence and data science', 'Natural language processing uses machine learning to understand text', 'Python programming language is essential for machine learning developers', 'Python libraries like TensorFlow and PyTorch simplify machine learning', 'Deep learning neural networks enable advanced AI applications']
```
混合搜索结合了**关键词匹配**（包含 "machine learning" 的文档）和**语义搜索**（与 "AI research" 语义相近的文档），通过 RRF（Reciprocal Rank Fusion）算法融合两路检索结果，返回最相关的文档。  
## 更多使用场景
安装 seekdb Claude Code 插件后，你可以向 Claude Code 询问各种 seekdb 相关问题：
### 基础查询
> 如何开始使用 seekdb？

> seekdb 支持哪些部署模式？
### 技术问题
> 如何在 seekdb 中创建向量索引？

> seekdb 的 AI 函数有哪些？如何使用 AI_EMBED 函数？

### 代码示例
> 展示一个使用 seekdb SQL 实现向量相似度搜索的示例

> 如何将 seekdb 与 LangChain 集成？

### 集成相关
> seekdb 如何配置 OpenAI 模型进行向量嵌入？

## 插件管理
### 验证安装
在 Claude Code 中运行 `/plugin` 命令，这将打开一个交互式界面，你可以浏览和管理已安装的插件。选择 "Manage and uninstall plugins" 以确认 `seekdb-plugin` 存在。  
### 更新插件
1. 运行 `/plugin` 打开插件管理界面
2. 使用方向键导航到 "Manage marketplaces"
3. 选择 `seekdb` 市场
4. 按 `u` 更新市场及其插件
### 故障排除
如果技能似乎无法正常工作：
1. **验证插件安装**：运行 /plugin 确认 seekdb-plugin 已安装
2. **重启 Claude Code**：完全关闭并重新打开 Claude Code 终端会话
3. **检查网络设置**：确保 `.claude/settings.local.json` 中已配置 `skipWebFetchPreflight: true`
## 工作原理
seekdb Claude Code 插件基于 Agent Skills 功能：
1. 技能注入：插件将 seekdb 官方文档和技能描述文件注入到 Claude Code
2. 自动调用：当你询问 seekdb 相关问题时，Claude Code 会自动检测并使用 seekdb 技能
3. 智能检索：Claude Code 会基于文档目录索引，精准定位相关文档并提供准确回答
与传统的手动查阅文档相比，这种方式让你可以在编程过程中随时获取精准的技术指导，而无需中断工作流程。
## 关于 Agent Skills
Agent Skills 允许将专业知识和工作流程打包成可重用的模块：
- 自动调用：技能会根据上下文由 Claude 自动调用，无需手动触发
- 模块化设计：每个技能独立维护，便于组织和管理
- 团队共享：通过 git 与团队共享专业知识和工作流程
- 可组合性：多个技能可以组合使用来解决复杂任务
了解更多关于 Agent Skills：
- [Agent Skills 概述](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [使用 Agent Skills 为智能体配备真实世界能力](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
## 总结
通过 **seekdb Claude Code 插件**，你可以在使用 Claude Code 进行开发时，随时获取 seekdb 的官方文档支持。无论是学习 seekdb 的新功能，还是解决开发中遇到的技术问题，Claude Code 都能基于最新的官方文档提供准确的指导。