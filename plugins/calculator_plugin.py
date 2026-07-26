import ast
import operator
from typing import ClassVar

from plugins.base_plugin import BasePlugin


class CalculatorPlugin(BasePlugin):

    name = "calculator"

    OPERATORS: ClassVar = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }

    def can_handle(self, command: str):
        keywords = (
            "+",
            "-",
            "*",
            "/",
            "%",
            "**",
            "plus",
            "minus",
            "times",
            "multiplied",
            "divided",
            "calculate",
            "what is",
            "x",
            "into",
        )

        return any(keyword in command.lower() for keyword in keywords)

    def execute(self, command: str):
        try:
            expression = self.prepare_expression(command)

            result = self.evaluate(expression)

            return f"The answer is {result}"

        except (
            SyntaxError,
            TypeError,
            ZeroDivisionError,
            ValueError,
            KeyError,
        ):
            return "I couldn't understand that mathematical expression."

    def prepare_expression(self, command: str):
        replacements = {
            "what is": "",
            "calculate": "",
            "plus": "+",
            "minus": "-",
            "times": "*",
            "multiplied by": "*",
            "x": "*",
            "into": "*",
            "divided by": "/",
            "over": "/",
        }

        expression = command.lower()

        for old, new in replacements.items():
            expression = expression.replace(old, new)

        return " ".join(expression.split())

    def evaluate(self, expression):
        node = ast.parse(
            expression,
            mode="eval",
        ).body

        return self._eval(node)

    def _eval(self, node):
        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)

            return self.OPERATORS[type(node.op)](
                left,
                right,
            )

        raise TypeError("Unsupported expression")