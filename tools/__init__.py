from tools.calculator import calculator_tool
from tools.registry import tool_registry
from tools.web_search import web_search_tool


tool_registry.register(calculator_tool)
tool_registry.register(web_search_tool)