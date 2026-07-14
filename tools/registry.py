from tools.base import BaseTool


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered"
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        tool = self._tools.get(name)

        if tool is None:
            raise KeyError(
                f"Tool '{name}' is not registered"
            )

        return tool

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())


tool_registry = ToolRegistry()