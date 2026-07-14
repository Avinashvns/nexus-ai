from models import ToolRequest
from tools import calculator_tool


def main():
    response = calculator_tool.execute(
        ToolRequest(
            input="10 + 5 * 2"
        )
    )

    print(response.model_dump())


if __name__ == "__main__":
    main()