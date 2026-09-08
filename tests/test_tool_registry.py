import contextlib
import io
import unittest

from tools.calculator_tool import CalculatorTool
from tools.tool_registry import ToolRegistry


class ToolRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()
        self.calculator = CalculatorTool()
        with contextlib.redirect_stdout(io.StringIO()):
            self.registry.register_tool(self.calculator)
            self.registry.register_function("echo", "Echo input", lambda text: text)

    def test_get_tool_returns_registered_object_or_none(self):
        self.assertIs(self.registry.get_tool("calculator"), self.calculator)
        self.assertIsNone(self.registry.get_tool("missing"))

    def test_execute_calculator_expression(self):
        self.assertEqual(self.registry.execute_tool("calculator", "15 * 8 + 32"), "152")

    def test_execute_function(self):
        self.assertEqual(self.registry.execute_tool("echo", "hello"), "hello")

    def test_execute_unknown_tool_raises_clear_error(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            self.registry.execute_tool("missing", "input")

    def test_execution_preserves_tool_errors(self):
        with self.assertRaises(ZeroDivisionError):
            self.registry.execute_tool("calculator", "1 / 0")

    def test_list_includes_tools_and_functions_and_returns_copy(self):
        names = self.registry.list_tools()
        self.assertEqual(names, ["calculator", "echo"])
        names.clear()
        self.assertEqual(self.registry.list_tools(), ["calculator", "echo"])

    def test_unregister_removes_tools_and_functions(self):
        self.assertTrue(self.registry.unregister("calculator"))
        self.assertIsNone(self.registry.get_tool("calculator"))
        self.assertFalse(self.registry.unregister("calculator"))
        self.assertTrue(self.registry.unregister("echo"))
        self.assertEqual(self.registry.list_tools(), [])
        self.assertEqual(self.registry.get_tools_description(), "暂无可用工具")
        with self.assertRaises(ValueError):
            self.registry.execute_tool("echo", "hello")

    def test_duplicate_name_prefers_tool_and_unregister_removes_both(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.registry.register_function("calculator", "Duplicate", lambda text: "other")
        self.assertEqual(self.registry.list_tools(), ["calculator", "echo"])
        self.assertEqual(self.registry.execute_tool("calculator", "2 + 3"), "5")
        self.assertTrue(self.registry.unregister("calculator"))
        with self.assertRaises(ValueError):
            self.registry.execute_tool("calculator", "2 + 3")
