from models import ToolRequest
from tools.web_search import web_search_tool


def main():
    response = web_search_tool.execute(
        ToolRequest(
            input="Agentic AI"
        )
    )

    assert response.success is True

    print(response.model_dump())


if __name__ == "__main__":
    main()