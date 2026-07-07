from agent.prompts import sub_agents_config
from tools.tavily_tools import tavily_internet_search

network_search_agent = {
    "name": sub_agents_config["tavily"].get("name", ""),
    "description": sub_agents_config["tavily"].get("description", ""),
    "system_prompt": sub_agents_config["tavily"].get("system_prompt", ""),
    "tools": [tavily_internet_search]
}
