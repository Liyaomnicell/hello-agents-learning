import unittest

from simple_agent import SimpleAgent


class FakeLLM:
    def __init__(self):
        self.calls = []

    def think(self, messages):
        self.calls.append(messages)
        return "Hello"


class SimpleAgentTests(unittest.TestCase):
    def test_run_sends_system_and_user_messages_and_records_history(self):
        llm = FakeLLM()
        agent = SimpleAgent("Assistant", llm, "Be helpful")

        self.assertEqual(agent.run("Hi"), "Hello")
        self.assertEqual(llm.calls, [[
            {"role": "system", "content": "Be helpful"},
            {"role": "user", "content": "Hi"},
        ]])
        self.assertEqual(agent.get_history(), [
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Hello"},
        ])
