import contextlib
import io
import unittest
from unittest.mock import patch


class AgentToolTests(unittest.TestCase):
    def test_agent_string_with_local_llm(self):
        from agent import Agent
        from my_llm import MyLLM

        class EchoAgent(Agent):
            def run(self, input_text, **kwargs):
                return input_text

        with patch("llm_client.OpenAI"):
            llm = MyLLM(model="demo", api_key="test", base_url="https://example.test/v1")
        self.assertEqual(str(EchoAgent("echo", llm)), "Agent(name=echo, model=demo)")

    def test_tool_parameter_defaults(self):
        from tools.tool_parameter import ToolParameter

        parameter = ToolParameter(name="text", type="string", description="Input text")
        self.assertTrue(parameter.required)
        self.assertIsNone(parameter.default)

    def test_tool_subclass_can_run(self):
        from tools.tool import Tool
        from tools.tool_parameter import ToolParameter

        class EchoTool(Tool):
            def run(self, parameters):
                return parameters["text"]

            def get_parameters(self):
                return [ToolParameter(name="text", type="string", description="Input text")]

        tool = EchoTool("echo", "Echo input")
        self.assertEqual(tool.run({"text": "hello"}), "hello")
        self.assertEqual(tool.get_parameters()[0].name, "text")

    def test_registry_describes_tools_and_functions(self):
        from tools.calculator_tool import CalculatorTool
        from tools.tool_registry import ToolRegistry

        registry = ToolRegistry()
        self.assertEqual(registry.get_tools_description(), "暂无可用工具")
        calculator = CalculatorTool()
        with contextlib.redirect_stdout(io.StringIO()):
            registry.register_tool(calculator)
            registry.register_function("echo", "Echo input", lambda text: text)
        self.assertEqual(
            registry.get_tools_description(),
            f"- calculator: {calculator.description}\n- echo: Echo input",
        )
