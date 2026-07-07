import os
from typing import Literal

from langchain_core.tools import tool

from dotenv import load_dotenv, find_dotenv
from tavily import TavilyClient

from api.monitor import monitor

# 自动加载环境变量文件.env
load_dotenv(find_dotenv())

# 初始化 Tavily 客户端
# 判断导入的类是否存在，存在则初始化，避免依赖缺失导致的异常
if TavilyClient:
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
else:
    monitor("Tavily API Key 未设置，将无法使用 Tavily 服务")
    tavily_client = None


@tool
def tavily_internet_search(
        query: str,
        max_results: int = 5,
        include_raw_content: bool = False,
        topic: Literal["general", "science", "finace"] = "general"
):
    """
    Tavily 网络搜索工具，根据问题进行网络查询，当需要获取外部互联网的公开信息、最新新闻或特定主题数据时使用此工具
    核心用途：
        当 AI Agent 需要获取外部互联网的公开信息、时效性数据（如新闻、金融动态）时调用，
        替代传统搜索引擎，返回更适配大模型的结构化结果。
    :param query: 搜索的核心问题/关键词，例如 "2026年AI行业政策"
    :param max_results: 控制返回结果数量，免费版建议不超过5
    :param include_raw_content: 是否返回详细新闻，False简略版本 True详细版本
    :param topic: 限定搜索内容类型，提升结果相关性
    :return:
        dict: Tavily API 返回的结构化结果，包含以下核心字段：
             - query: 原始搜索词
             - results: 搜索结果列表，每个元素包含 url、content（摘要）、raw_content（原始内容，可选）等
             - str: 初始化失败时返回错误提示字符串
     异常处理：
         捕获搜索过程中的所有异常并重新抛出，确保 Agent 能感知到搜索失败并处理
    """
    if not tavily_client:
        return "Tavily_Client 未初始化"

    monitor.report_tool("网络搜素工具", {"网络搜索工具：Tavily_Client": query})

    try:
        results = tavily_client.search(
            query=query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic
        )
        return results
    except Exception as e:
        monitor.report_error("Tavily 搜索工具", e)
        raise e
