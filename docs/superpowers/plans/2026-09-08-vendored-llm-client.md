# Vendored LLM Client Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the project own its LLM client source and remove the runtime path dependency on the Chapter 4 directory.

**Architecture:** Add `llm_client.py` as a project-local copy of the Chapter 4 client. `MyLLM` imports and subclasses that local class normally, so the public `MyLLM()` call site remains unchanged.

**Tech Stack:** Python 3.14, OpenAI SDK, python-dotenv, unittest.

---

### Task 1: Vendor and use the local LLM client

**Files:**
- Create: `llm_client.py`
- Modify: `my_llm.py`
- Modify: `tests/test_local_imports.py`

- [ ] **Step 1: Write the failing test**

```python
def test_my_llm_inherits_the_local_client():
    assert MyLLM.__mro__[1].__module__ == "llm_client"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `.venv/bin/python -m unittest tests/test_local_imports.py -v`

Expected: FAIL because `MyLLM` currently inherits from `chapter4_llm_client`.

- [ ] **Step 3: Add the local source and replace the dynamic import**

Copy the complete Chapter 4 `HelloAgentsLLM` implementation into
`llm_client.py`. Replace `my_llm.py` with:

```python
from llm_client import HelloAgentsLLM


class MyLLM(HelloAgentsLLM):
    """Backward-compatible name for the project-local LLM client."""
```

- [ ] **Step 4: Run full verification**

Run: `.venv/bin/python -m unittest discover -s tests -v && .venv/bin/python -m py_compile llm_client.py my_llm.py simple_agent.py calculator_tool.py first-test.py my_main.py`

Expected: all tests PASS and compilation produces no output.
