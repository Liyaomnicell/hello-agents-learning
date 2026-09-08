# hello-agents-learning

## MyLLM usage

`MyLLM` supports any OpenAI-compatible endpoint:

```python
from my_llm import MyLLM

llm = MyLLM(
    model="your-model-id",
    api_key="your-api-key",
    base_url="https://provider.example/v1",
    timeout=90,
)
```

Any omitted value falls back to the corresponding environment variable, loaded
from `.env`:

```dotenv
LLM_MODEL_ID=your-model-id
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://provider.example/v1
LLM_TIMEOUT=60
```

With these values configured in `.env`, initialize the client with `llm = MyLLM()`.
The timeout is in seconds and defaults to `60` when omitted from both the
constructor and the environment.
