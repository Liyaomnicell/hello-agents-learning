# OpenAI-Compatible MyLLM Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let `MyLLM` configure any OpenAI-compatible endpoint using standard Python parameter names.

**Architecture:** `MyLLM` remains a subclass of local `HelloAgentsLLM` and translates `api_key`/`base_url` into the parent's existing `apiKey`/`baseUrl` parameters. Unspecified values continue to be supplied by the local client's `LLM_*` environment variables.

**Tech Stack:** Python 3.14, unittest, OpenAI SDK.

---

### Task 1: Add explicit OpenAI-compatible configuration

**Files:**
- Modify: `tests/test_local_imports.py`
- Modify: `my_llm.py`

- [ ] **Step 1: Write the failing test**

```python
from unittest.mock import patch

@patch("llm_client.OpenAI")
def test_my_llm_accepts_standard_openai_configuration(self, openai_client):
    MyLLM(model="demo", api_key="key", base_url="https://example.test/v1", timeout=90)
    openai_client.assert_called_once_with(
        api_key="key", base_url="https://example.test/v1", timeout=90
    )
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `.venv/bin/python -m unittest tests/test_local_imports.py -v`

Expected: FAIL because `MyLLM` does not accept `api_key` or `base_url`.

- [ ] **Step 3: Implement the adapter**

```python
def __init__(self, model=None, api_key=None, base_url=None, timeout=None):
    super().__init__(model=model, apiKey=api_key, baseUrl=base_url, timeout=timeout)
```

- [ ] **Step 4: Run full verification**

Run: `.venv/bin/python -m unittest discover -s tests -v && .venv/bin/python -m py_compile llm_client.py my_llm.py simple_agent.py calculator_tool.py first-test.py my_main.py`

Expected: all tests PASS and compilation produces no output.
