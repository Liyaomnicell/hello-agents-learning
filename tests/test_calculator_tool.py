import unittest

from tools.calculator_tool import CalculatorTool


class CalculatorToolTests(unittest.TestCase):
    def test_calculator_evaluates_basic_arithmetic(self):
        self.assertEqual(CalculatorTool().run("2 + 3 * 4"), "14")
