# 目标加载yml中的数据，供创建主和子智能体使用
import yaml # yaml配置文件读取
from pathlib import Path

# 定义一个加载函数，配置文件yaml加载成字典
def load_yaml(file_path):
    """
    读取并加载YAML格式的提示词配置文件
    Args:
        file_path (str/Path): YAML配置文件的路径
    Returns:
        dict: 解析后的YAML配置字典，包含主智能体和子智能体的提示词配置
    """
    with open(file_path, 'r', encoding='utf-8') as file :
        """
        这是 safe_load 区别于 load 的核心（也是为什么必须用它）：
        yaml.load()：不安全，会解析 YAML 中的「自定义对象 / 执行代码」，如果加载的 YAML 文件被恶意篡改（比如插入了执行系统命令的代码），会导致服务器被攻击、数据泄露；
        yaml.safe_load()：仅解析 YAML 标准数据类型（字符串、数字、字典、列表、布尔值等），完全禁止解析 / 执行任何自定义对象、函数、代码，从根源避免安全风险。
        """
        return yaml.safe_load(file)

# 获取当前脚本文件的父级目录的上一级（项目根目录）
# Path(__file__)：当前脚本文件的绝对路径
# parents[1]：向上追溯两级目录，定位到项目根目录(索引时从0开始的)
project_root_path  = Path(__file__).parents[1]

# 拼接提示词配置文件的完整路径（根目录/prompt/prompts.yml）
yaml_file_path = project_root_path / "prompt" / "prompts.yml"
# 加载YAML配置文件内容
prompt_yaml_content = load_yaml(yaml_file_path)
print(f"YAML配置加载完成，文件内容: {prompt_yaml_content}\n")

main_agent_config = prompt_yaml_content["main_agent"]
sub_agents_config = prompt_yaml_content["sub_agents"]

print(f"main_agent_config: {main_agent_config} , \nsub_agents_config: {sub_agents_config}")