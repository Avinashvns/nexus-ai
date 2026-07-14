from core.logger import app_logger
from models import ToolRequest, ToolResponse
from tools.registry import tool_registry


class ToolExecutor:
    def execute(
        self,
        tool_name: str,
        request: ToolRequest,
    ) -> ToolResponse:
        try:
            app_logger.info(
                f"Executing tool: {tool_name}"
            )

            tool = tool_registry.get(tool_name)

            response = tool.execute(request)

            app_logger.success(
                f"Tool executed successfully: {tool_name}"
            )

            return response

        except Exception as error:
            app_logger.error(
                f"Tool execution failed: {tool_name} - {error}"
            )

            return ToolResponse(
                success=False,
                output=None,
                metadata={
                    "tool": tool_name,
                    "error": str(error),
                },
            )


tool_executor = ToolExecutor()