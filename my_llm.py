"""Expose the Chapter 4 LLM client through the project's existing name."""

import importlib.util
from pathlib import Path


_CLIENT_PATH = (
    Path(__file__).resolve().parent / ".." / "hello-agents" / "code" / "chapter4" / "llm_client.py"
).resolve()
_SPEC = importlib.util.spec_from_file_location("chapter4_llm_client", _CLIENT_PATH)

if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Unable to load Chapter 4 LLM client from {_CLIENT_PATH}")

_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)


class MyLLM(_MODULE.HelloAgentsLLM):
    """Backward-compatible name for the local Chapter 4 LLM client."""
