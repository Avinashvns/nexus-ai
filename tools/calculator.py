import ast
import operator
from typing import Any

from models import ToolRequest, ToolResponse
from tools.base import BaseTool


class CalculatorTool(BaseTool):
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def __init__(self):
        super().__init__(name="CalculatorTool")

    def execute(self, request: ToolRequest) -> ToolResponse:
        try:
            expression = str(request.input).strip()

            if not expression:
                raise ValueError("Expression cannot be empty")

            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body)

            return ToolResponse(
                success=True,
                output=result,
                metadata={
                    "tool": self.name,
                    "expression": expression,
                },
            )

        except Exception as error:
            return ToolResponse(
                success=False,
                output=None,
                metadata={
                    "tool": self.name,
                    "error": str(error),
                },
            )

    def _evaluate(self, node: ast.AST) -> Any:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numbers are allowed")

        if isinstance(node, ast.BinOp):
            operator_function = self.OPERATORS.get(type(node.op))

            if operator_function is None:
                raise ValueError("Operator is not allowed")

            return operator_function(
                self._evaluate(node.left),
                self._evaluate(node.right),
            )

        if isinstance(node, ast.UnaryOp):
            operator_function = self.OPERATORS.get(type(node.op))

            if operator_function is None:
                raise ValueError("Operator is not allowed")

            return operator_function(
                self._evaluate(node.operand)
            )

        raise ValueError("Invalid mathematical expression")


calculator_tool = CalculatorTool()