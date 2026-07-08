# Deep Search

> 基于多智能体架构的深度搜索系统，集成网络搜索、数据库查询与知识库问答能力。

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](./LICENSE)
[![Framework](https://img.shields.io/badge/Framework-LangChain%20%2B%20DeepAgents-orange.svg)](https://github.com/langchain-ai/langchain)

## 项目简介

Deep Search 是一个多智能体协作的 AI 搜索系统，通过主智能体（Main Agent）协调三个专业子智能体（Sub-Agent），实现对互联网信息、企业数据库和内部知识库的统一检索与分析。

系统基于 **LangChain + LangGraph + DeepAgents** 构建多智能体编排能力，使用 **FastAPI** 提供 Web 服务，支持流式输出、会话隔离和实时监控。

## 核心特性

- **多智能体协作** — 主智能体根据任务自动调度子智能体，各司其职
- **三大检索引擎** — 网络搜索、数据库查询、知识库问答一站式集成
- **会话级隔离** — 基于 `ContextVar` 实现异步并发下的请求隔离，杜绝数据串台
- **实时监控** — 工具调用全程埋点，支持 WebSocket 实时推送执行进度
- **文件处理** — 支持 Markdown / Word / PDF / Excel 文件读取与 Markdown→PDF 转换
- **YAML 驱动配置** — 智能体提示词通过 YAML 文件管理，无需改代码即可调优

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     Main Agent                          │
│         (主智能体 / 任务协调器)                           │
│                                                         │
│   工具: generate_markdown | convert_md_to_pdf           │
│         read_file_content                               │
├──────────┬──────────────────┬──────────────────────────┤
│          │                  │                          │
▼          ▼                  ▼                          │
┌────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│ 网络搜索    │  │  数据库查询       │  │  知识库问答     │ │
│ Sub-Agent  │  │  Sub-Agent       │  │  Sub-Agent     │ │
│            │  │                  │  │                │ │
│ Tavily API │  │  MySQL           │  │  RAGFlow SDK   │ │
│ internet_  │  │  list_tables     │  │  get_assistant │ │
│ search     │  │  get_table_data  │  │  create_ask    │
│            │  │  execute_sql     │  │  _delete       │ │
└────────────┘  └──────────────────┘  └────────────────┘ │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    API 基础设施层                         │
│  context.py  (会话隔离)  │  monitor.py (监控埋点)        │
│  logger.py   (日志追踪)  │  path_utils (路径解析)        │
└─────────────────────────────────────────────────────────┘
```

## 技术栈

| 类别 | 技术 |
|------|------|
| LLM 编排 | LangChain, LangGraph, DeepAgents |
| Web 框架 | FastAPI, Uvicorn |
| 网络搜索 | Tavily Python SDK |
| 数据库 | MySQL Connector/Python |
| 知识库 | RAGFlow SDK |
| 文件处理 | python-docx, pypdf, openpyxl, pandas |
| 配置管理 | python-dotenv, PyYAML |
| Python | >= 3.12 |

## 项目结构

```
deep-search/
├── agent/                          # 智能体定义
│   ├── __init__.py
│   ├── llm.py                      # LLM 模型初始化
│   ├── main_agent.py               # 主智能体（协调器）
│   ├── prompts.py                  # YAML 提示词加载器
│   └── sub_agents/                 # 子智能体
│       ├── __init__.py
│       ├── network_search_agent.py # 网络搜索助手
│       ├── database_query_agent.py # 数据库查询助手
│       └── knowledge_base_agent.py # 知识库问答助手
├── api/                            # API 基础设施层
│   ├── __init__.py
│   ├── context.py                  # 会话上下文隔离（ContextVar）
│   ├── monitor.py                  # 工具监控与 WebSocket 推送
│   └── logger.py                   # Agent 日志与回调追踪
├── tools/                          # Agent 工具集
│   ├── __init__.py
│   ├── markdown_tools.py           # Markdown 文件生成
│   ├── mysql_tools.py              # MySQL 数据库操作
│   ├── pdf_tools.py                # Markdown → PDF 转换
│   ├── ragflow_tools.py            # RAGFlow 知识库操作
│   ├── tavily_tools.py             # Tavily 网络搜索
│   └── upload_file_read_tool.py    # 多格式文件读取
├── utils/                          # 工具函数
│   ├── __init__.py
│   ├── path_utils.py               # 路径解析与会话目录隔离
│   └── word_converter.py           # Word 引擎 PDF 转换
├── prompt/                         # 提示词配置
│   └── prompts.yml                 # 主/子智能体提示词定义
├── .gitignore
├── LICENSE
├── pyproject.toml
├── uv.lock
└── README.md
```

## 快速开始

### 环境要求

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (推荐) 或 pip
- MySQL 数据库
- RAGFlow 服务（已部署）
- Tavily API Key（[申请地址](https://tavily.com)）
- OpenAI 兼容的 LLM 服务端点

### 安装

```bash
# 克隆项目
git clone <repository-url>
cd deep-search

# 使用 uv 安装依赖（推荐）
uv sync

# 或使用 pip
pip install -e .
```

### 配置

在项目根目录创建 `.env` 文件，填入以下配置项（**请勿将 .env 提交至版本控制**）：

```env
# ========== LLM 配置 ==========
# OpenAI 兼容的模型名称
LLM_QWEN_MAX=your-model-name

# ========== Tavily 网络搜索 ==========
TAVILY_API_KEY=your-tavily-api-key

# ========== RAGFlow 知识库 ==========
RAGFLOW_API_KEY=your-ragflow-api-key
RAGFLOW_API_URL=https://your-ragflow-server.com

# ========== MySQL 数据库 ==========
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your-mysql-user
MYSQL_PASSWORD=your-mysql-password
MYSQL_DATABASE=your-database-name
MYSQL_CHARSET=utf8mb4
MYSQL_COLLATION=utf8mb4_unicode_ci
MYSQL_SQL_MODE=TRADITIONAL
```

> **安全提示**：`.env` 文件已在 `.gitignore` 中忽略。请确保不要在实际环境中使用上述示例值。

### 提示词配置

智能体的系统提示词通过 `prompt/prompts.yml` 管理，可根据业务需求自定义：

```yaml
main_agent:
  system_prompt: |
    你的主智能体提示词...

sub_agents:
  tavily:
    name: "网络搜索助手"
    description: "..."
    system_prompt: |
      你的子智能体提示词...
  db:
    name: "数据库查询助手"
    description: "..."
    system_prompt: |
      ...
  ragflow:
    name: "RAGFlow助手"
    description: "..."
    system_prompt: |
      ...
```

## 使用方式

### 初始化智能体

```python
from agent.main_agent import main_agent

# main_agent 已在导入时自动初始化
# 包含三个子智能体和文件处理工具
```

### 工具说明

| 工具 | 所属 | 功能 |
|------|------|------|
| `tavily_internet_search` | 网络搜索子智能体 | 通过 Tavily API 进行互联网搜索 |
| `list_sql_tables` | 数据库查询子智能体 | 列出 MySQL 数据库中所有表 |
| `get_table_data` | 数据库查询子智能体 | 读取指定表前 100 行数据（CSV 格式） |
| `execute_sql_query` | 数据库查询子智能体 | 执行自定义 SQL 查询 |
| `get_assistant_list` | 知识库子智能体 | 获取 RAGFlow 聊天助手列表 |
| `create_ask_delete` | 知识库子智能体 | 向指定助手提问（临时会话，用完即删） |
| `generate_markdown` | 主智能体 | 生成 Markdown 文件 |
| `convert_md_to_pdf` | 主智能体 | 将 Markdown 转换为 PDF |
| `read_file_content` | 主智能体 | 读取 MD/DOCX/PDF/XLSX 文件内容 |

### 会话隔离机制

系统使用 Python `ContextVar` 实现异步并发下的会话隔离：

```python
from api.context import set_session_context, reset_session_context, set_thread_context

# 请求开始时设置上下文
session_token = set_session_context("/data/session_123")
thread_token = set_thread_context("thread_001")

try:
    # 执行 Agent 任务...
    # 任何深层调用都能通过 get_session_context() 获取当前会话目录
    pass
finally:
    # 请求结束时清理上下文
    reset_session_context(session_token, thread_token)
```

### 监控与日志

```python
from api.monitor import monitor
from api.logger import AgentLogger, AgentLogCallbackHandler

# 工具监控（支持 WebSocket 实时推送）
monitor.report_tool("工具名称", {"参数": "值"})

# Agent 日志追踪
logger = AgentLogger(thread_id="xxx", project_root="./")
# 配合 LangChain Callback 使用
```

## 开发说明

### 路径解析

文件工具使用 `utils/path_utils.py` 中的 `resolve_path` 进行统一路径解析，支持：

- 虚拟路径前缀清洗（`/workspace`, `/mnt/data`, `/home/user`）
- `updated/` 目录特殊处理（用户上传文件）
- 会话目录隔离与路径嵌套防护
- Windows / Linux 跨平台兼容

### 新增子智能体

1. 在 `agent/sub_agents/` 下创建新文件
2. 从 `agent.prompts` 加载配置
3. 绑定所需工具
4. 在 `agent/main_agent.py` 的 `subagents_list` 中注册

### 新增工具

1. 在 `tools/` 下创建工具文件
2. 使用 `@tool` 装饰器（来自 `langchain_core.tools`）定义工具
3. 添加 `monitor.report_tool()` 埋点
4. 在对应智能体配置中注册

## 许可证

本项目基于 [Apache License 2.0](./LICENSE) 开源。
