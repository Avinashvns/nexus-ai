from tools.selector import tool_selector


def test_valid_selection():
    selection = {
        "tool": "CalculatorTool",
        "input": "25 * 18",
    }

    assert tool_selector.validate_selection(selection) is True


def test_unknown_tool():
    selection = {
        "tool": "UnknownTool",
        "input": "25 * 18",
    }

    assert tool_selector.validate_selection(selection) is False


def test_missing_input():
    selection = {
        "tool": "CalculatorTool",
    }

    assert tool_selector.validate_selection(selection) is False


def main():
    test_valid_selection()
    test_unknown_tool()
    test_missing_input()

    response = tool_selector.execute(
        "Calculate 25 * 18"
    )

    print(response.model_dump())


if __name__ == "__main__":
    main()