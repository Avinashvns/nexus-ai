from unittest.mock import patch

from agents.search import search_agent
from models import AgentRequest, ToolResponse


def main():
    empty_response = ToolResponse(
        success=True,
        output=[],
        metadata={
            "tool": "WebSearchTool",
        },
    )

    with patch(
        "agents.search.tool_executor.execute",
        return_value=empty_response,
    ):
        response = search_agent.run(
            AgentRequest(
                task="Unknown search query"
            )
        )

    assert response.success is False

    assert (
        response.metadata["error"]
        == "No web search results found"
    )

    print(response.model_dump())

    print(
        "\nSearch Reliability Test Passed"
    )


if __name__ == "__main__":
    main()