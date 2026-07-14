from models import ToolRequest, ToolResponse
from tools.base import BaseTool
from tools.executor import tool_executor
from tools.registry import tool_registry


class DemoTool(BaseTool):
    def execute(self, request: ToolRequest) -> ToolResponse:
        return ToolResponse(
            success=True,
            output=f"Executed: {request.input}",
        )


def main():
    tool = DemoTool("DemoTool")

    tool_registry.register(tool)

    response = tool_executor.execute(
        tool_name="DemoTool",
        request=ToolRequest(
            input="Hello Nexus"
        ),
    )

    print(response.model_dump())


if __name__ == "__main__":
    main()