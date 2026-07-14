from agents.base import BaseAgent
from core.logger import app_logger
from models import AgentRequest, AgentResponse, ToolRequest
from tools.executor import tool_executor

import tools


class SearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="SearchAgent")

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        try:
            app_logger.info(
                f"{self.name} searching web"
            )

            tool_response = tool_executor.execute(
                tool_name="WebSearchTool",
                request=ToolRequest(
                    input=request.task,
                    context=request.context,
                ),
            )

            if not tool_response.success:
                raise RuntimeError(
                    tool_response.metadata.get(
                        "error",
                        "Web search failed",
                    )
                )

            results = tool_response.output

            if not results:
                raise RuntimeError(
                    "No web search results found"
                )

            valid_results = []

            for result in results:
                if not isinstance(result, dict):
                    continue

                content = result.get("content", "").strip()

                if not content:
                    continue

                valid_results.append(result)

            if not valid_results:
                raise RuntimeError(
                    "No valid web search results found"
                )

            results = valid_results

            app_logger.success(
                f"{self.name} found {len(results)} results"
            )

            return AgentResponse(
                success=True,
                output=results,
                metadata={
                    "agent": self.name,
                    "result_count": len(results),
                    "validated": True,
                },
            )

        except Exception as error:
            app_logger.error(
                f"{self.name} Error: {error}"
            )

            return AgentResponse(
                success=False,
                output=[],
                metadata={
                    "agent": self.name,
                    "error": str(error),
                },
            )


search_agent = SearchAgent()