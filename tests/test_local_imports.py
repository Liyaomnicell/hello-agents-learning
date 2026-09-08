import unittest

from my_llm import MyLLM


class LocalImportTests(unittest.TestCase):
    def test_my_llm_inherits_the_chapter4_client(self):
        self.assertEqual(MyLLM.__mro__[1].__module__, "chapter4_llm_client")
