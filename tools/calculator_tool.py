"""A safe arithmetic tool for local agent examples."""

import ast
import operator


class CalculatorTool:
    """Evaluate numeric arithmetic without executing arbitrary Python code."""

    name = "calculator"
    description = "Evaluate arithmetic using +, -, *, /, %, **, and parentheses."
    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    def run(self, expression):
        """Return the result of a numeric arithmetic expression as text."""
        try:
            expression_node = ast.parse(expression, mode="eval").body
        except SyntaxError as error:
            raise ValueError("Only numeric arithmetic expressions are supported") from error
        return str(self._evaluate(expression_node))

    def _evaluate(self, node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in self._operators:
            operation = self._operators[type(node.op)]
            return operation(self._evaluate(node.left), self._evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = self._evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        raise ValueError("Only numeric arithmetic expressions are supported")
