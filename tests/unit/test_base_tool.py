from models import ToolRequest, ToolResponse
from tools.base import BaseTool


class DemoTool(BaseTool):
    def execute(self, request: ToolRequest) -> ToolResponse:
        return ToolResponse(
            success=True,
            output=f"Tool received: {request.input}",
        )


def main():
    tool = DemoTool("Demo Tool")

    request = ToolRequest(input="Hello Tool")

    response = tool.execute(request)

    print(response.model_dump())


if __name__ == "__main__":
    main()