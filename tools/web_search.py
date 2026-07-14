from ddgs import DDGS

from models import ToolRequest, ToolResponse
from tools.base import BaseTool


class WebSearchTool(BaseTool):
    def __init__(self):
        super().__init__(name="WebSearchTool")

    def execute(
        self,
        request: ToolRequest,
    ) -> ToolResponse:
        try:
            query = str(request.input).strip()

            if not query:
                raise ValueError(
                    "Search query cannot be empty"
                )

            search_results = DDGS().text(
                query=query,
                max_results=5,
            )

            results: list[dict] = []

            for result in search_results:
                content = result.get(
                    "body",
                    "",
                ).strip()

                if not content:
                    continue

                results.append(
                    {
                        "title": result.get(
                            "title",
                            "",
                        ),
                        "content": content,
                        "url": result.get(
                            "href",
                            "",
                        ),
                    }
                )

            return ToolResponse(
                success=True,
                output=results,
                metadata={
                    "tool": self.name,
                    "query": query,
                    "result_count": len(results),
                },
            )

        except Exception as error:
            return ToolResponse(
                success=False,
                output=[],
                metadata={
                    "tool": self.name,
                    "error": str(error),
                },
            )


web_search_tool = WebSearchTool()