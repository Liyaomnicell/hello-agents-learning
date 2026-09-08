import unittest
from unittest.mock import patch

from my_llm import MyLLM


class LocalImportTests(unittest.TestCase):
    def test_my_llm_inherits_the_local_client(self):
        self.assertEqual(MyLLM.__mro__[1].__module__, "llm_client")

    @patch("llm_client.OpenAI")
    def test_my_llm_accepts_standard_openai_configuration(self, openai_client):
        MyLLM(
            model="demo",
            api_key="key",
            base_url="https://example.test/v1",
            timeout=90,
        )

        openai_client.assert_called_once_with(
            api_key="key",
            base_url="https://example.test/v1",
            timeout=90,
        )
