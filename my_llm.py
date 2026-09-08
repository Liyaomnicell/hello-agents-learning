"""Expose the project-local LLM client through the existing name."""

from llm_client import HelloAgentsLLM


class MyLLM(HelloAgentsLLM):
    """Configure any OpenAI-compatible endpoint with standard argument names."""

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: int | None = None,
    ):
        super().__init__(
            model=model,
            apiKey=api_key,
            baseUrl=base_url,
            timeout=timeout,
        )
