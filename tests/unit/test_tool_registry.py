from models import ToolRequest, ToolResponse
from tools.base import BaseTool
from tools.registry import ToolRegistry


class DemoTool(BaseTool):
    def execute(self, request: ToolRequest) -> ToolResponse:
        return ToolResponse(
            success=True,
            output=request.input,
        )


def main():
    registry = ToolRegistry()

    tool = DemoTool("DemoTool")

    registry.register(tool)

    print(registry.list_tools())

    registered_tool = registry.get("DemoTool")

    response = registered_tool.execute(
        ToolRequest(input="Hello Nexus")
    )

    print(response.model_dump())


if __name__ == "__main__":
    main()