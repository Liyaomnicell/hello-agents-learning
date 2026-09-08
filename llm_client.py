"""An OpenAI-compatible streaming LLM client owned by this project."""

import os
from typing import Dict, Iterator, List

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class HelloAgentsLLM:
    """Call an OpenAI-compatible LLM API and collect its streamed response."""

    def __init__(
        self,
        model: str | None = None,
        apiKey: str | None = None,
        baseUrl: str | None = None,
        timeout: int | None = None,
    ):
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

    def stream_invoke(
        self, messages: List[Dict[str, str]], temperature: float = 0
    ) -> Iterator[str]:
        """Yield text chunks without printing, closing the API stream when done."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        try:
            for chunk in response:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        finally:
            response.close()

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """Send messages and return the full text while printing streamed tokens."""
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            collected_content = []
            for content in self.stream_invoke(messages, temperature=temperature):
                print(content, end="", flush=True)
                collected_content.append(content)
            print()
            print("✅ 大语言模型响应成功")
            return "".join(collected_content)

        except Exception as error:
            print(f"❌ 调用LLM API时发生错误: {error}")
            raise
