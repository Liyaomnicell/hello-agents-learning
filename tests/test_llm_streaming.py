import contextlib
import io
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from my_llm import MyLLM
from my_simple_agent import MySimpleAgent


def chunk(content):
    return SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=content))])


class FakeStream:
    def __init__(self, chunks):
        self.chunks = iter(chunks)
        self.closed = False

    def __iter__(self):
        return self.chunks

    def close(self):
        self.closed = True


class LLMStreamingTests(unittest.TestCase):
    def setUp(self):
        patcher = patch("llm_client.OpenAI")
        self.client = patcher.start().return_value
        self.addCleanup(patcher.stop)
        self.llm = MyLLM(model="demo", api_key="test", base_url="https://example.test/v1")
        self.messages = [{"role": "user", "content": "Hi"}]

    def test_stream_yields_text_incrementally_and_skips_empty_chunks(self):
        consumed = []

        def chunks():
            yield SimpleNamespace(choices=[])
            yield chunk(None)
            yield chunk("")
            yield chunk("Hello")
            consumed.append("second")
            yield chunk(" world")

        stream = FakeStream(chunks())
        self.client.chat.completions.create.return_value = stream
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            response = self.llm.stream_invoke(self.messages, temperature=0.5)
            self.assertEqual(next(response), "Hello")
            self.assertEqual(consumed, [])
            self.assertEqual(list(response), [" world"])
        self.assertEqual(output.getvalue(), "")
        self.assertTrue(stream.closed)
        self.client.chat.completions.create.assert_called_once_with(
            model="demo", messages=self.messages, temperature=0.5, stream=True,
        )

    def test_closing_generator_closes_api_stream(self):
        stream = FakeStream([chunk("first"), chunk("second")])
        self.client.chat.completions.create.return_value = stream
        response = self.llm.stream_invoke(self.messages)
        self.assertEqual(next(response), "first")
        response.close()
        self.assertTrue(stream.closed)

    def test_stream_error_propagates_and_closes_connection(self):
        def chunks():
            yield chunk("partial")
            raise RuntimeError("stream interrupted")

        stream = FakeStream(chunks())
        self.client.chat.completions.create.return_value = stream
        response = self.llm.stream_invoke(self.messages)
        self.assertEqual(next(response), "partial")
        with self.assertRaisesRegex(RuntimeError, "stream interrupted"):
            next(response)
        self.assertTrue(stream.closed)

    def test_think_returns_complete_text_and_prints_it_once(self):
        stream = FakeStream([chunk("Hello"), chunk(" world")])
        self.client.chat.completions.create.return_value = stream
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(self.llm.think(self.messages), "Hello world")
        self.assertEqual(output.getvalue().count("Hello world"), 1)
        self.assertTrue(stream.closed)

    def test_agent_stream_records_complete_response_in_history(self):
        self.client.chat.completions.create.return_value = FakeStream([chunk("Hello"), chunk(" world")])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            agent = MySimpleAgent("demo", self.llm, "Be helpful")
            self.assertEqual(list(agent.stream_run("Hi")), ["Hello", " world"])
        self.assertEqual(output.getvalue().count("Hello world"), 1)
        self.assertEqual(
            [message.to_dict() for message in agent.get_history()],
            [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello world"}],
        )
