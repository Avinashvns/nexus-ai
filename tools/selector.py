import json
from typing import Any

import tools

from core.logger import app_logger
from llm.router import llm_router
from models import ToolRequest, ToolResponse
from tools.executor import tool_executor
from tools.registry import tool_registry


class ToolSelector:
    REQUIRED_FIELDS = {
        "tool",
        "input",
    }

    def validate_selection(self, selection: Any) -> bool:
        if not isinstance(selection, dict):
            return False

        if not self.REQUIRED_FIELDS.issubset(selection):
            return False

        if selection["tool"] not in tool_registry.list_tools():
            return False

        if selection["input"] is None:
            return False

        return True

    def select(self, task: str) -> dict:
        available_tools = tool_registry.list_tools()

        prompt = f"""
You are a tool selection system.

Available tools:
{available_tools}

CalculatorTool:
Use for mathematical calculations.

User Task:
{task}

Return ONLY valid JSON.

Format:
{{
    "tool": "CalculatorTool",
    "input": "mathematical expression"
}}

Do not return markdown.
Do not return explanations.
"""

        response = llm_router.generate(prompt)

        selection = json.loads(response)

        if not self.validate_selection(selection):
            raise ValueError("Invalid tool selection")

        return selection

    def execute(self, task: str) -> ToolResponse:
        try:
            selection = self.select(task)

            tool_name = selection["tool"]
            tool_input = selection["input"]

            app_logger.info(
                f"LLM selected tool: {tool_name}"
            )

            return tool_executor.execute(
                tool_name=tool_name,
                request=ToolRequest(input=tool_input),
            )

        except Exception as error:
            app_logger.error(
                f"Tool selection failed: {error}"
            )

            return ToolResponse(
                success=False,
                output=None,
                metadata={
                    "error": str(error),
                },
            )


tool_selector = ToolSelector()