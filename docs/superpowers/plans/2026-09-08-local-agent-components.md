# Local Agent Components Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the learning scripts' installed `hello-agents` dependency with local LLM, agent, and calculator components.

**Architecture:** `my_llm.py` dynamically loads the existing Chapter 4 client using its absolute path and exposes it through the existing `MyLLM` name. `simple_agent.py` handles prompt/history orchestration, while `calculator_tool.py` evaluates only a constrained Python AST expression grammar.

**Tech Stack:** Python 3.14 standard library, OpenAI SDK through the Chapter 4 client, `unittest`.

---

### Task 1: Test and implement the local simple agent

**Files:**
- Create: `tests/test_simple_agent.py`
- Create: `simple_agent.py`

- [ ] **Step 1: Write the failing test**

```python
from simple_agent import SimpleAgent


class FakeLLM:
    def __init__(self):
        self.calls = []

    def think(self, messages):
        self.calls.append(messages)
        return "Hello"


def test_run_sends_system_and_user_messages_and_records_history():
    llm = FakeLLM()
    agent = SimpleAgent("Assistant", llm, "Be helpful")

    assert agent.run("Hi") == "Hello"
    assert llm.calls == [[
        {"role": "system", "content": "Be helpful"},
        {"role": "user", "content": "Hi"},
    ]]
    assert agent.get_history() == [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello"},
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_simple_agent.py -v`

Expected: FAIL because `simple_agent` does not exist.

- [ ] **Step 3: Write the minimal implementation**

```python
class SimpleAgent:
    def __init__(self, name, llm, system_prompt):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self._history = []

    def run(self, user_prompt):
        messages = [{"role": "system", "content": self.system_prompt}, *self._history,
                    {"role": "user", "content": user_prompt}]
        response = self.llm.think(messages) or ""
        self._history.extend((
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": response},
        ))
        return response

    def get_history(self):
        return list(self._history)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_simple_agent.py -v`

Expected: PASS.

### Task 2: Test and implement the safe calculator

**Files:**
- Create: `tests/test_calculator_tool.py`
- Create: `calculator_tool.py`

- [ ] **Step 1: Write the failing test**

```python
from calculator_tool import CalculatorTool


def test_calculator_evaluates_basic_arithmetic():
    assert CalculatorTool().run("2 + 3 * 4") == "14"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_calculator_tool.py -v`

Expected: FAIL because `calculator_tool` does not exist.

- [ ] **Step 3: Write the minimal implementation**

```python
import ast
import operator


class CalculatorTool:
    name = "calculator"
    description = "Evaluate arithmetic expressions using +, -, *, /, %, **, and parentheses."
    _operators = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
                  ast.Div: operator.truediv, ast.Mod: operator.mod, ast.Pow: operator.pow}

    def run(self, expression):
        return str(self._evaluate(ast.parse(expression, mode="eval").body))

    def _evaluate(self, node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in self._operators:
            return self._operators[type(node.op)](self._evaluate(node.left), self._evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = self._evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        raise ValueError("Only numeric arithmetic expressions are supported")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_calculator_tool.py -v`

Expected: PASS.

### Task 3: Replace imports in the example scripts

**Files:**
- Modify: `my_llm.py`
- Modify: `first-test.py`
- Test: `tests/test_local_imports.py`

- [ ] **Step 1: Write the failing test**

```python
from my_llm import MyLLM


def test_my_llm_inherits_the_chapter4_client():
    assert MyLLM.__mro__[1].__module__ == "chapter4_llm_client"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_local_imports.py -v`

Expected: FAIL because the current parent class comes from `hello_agents`.

- [ ] **Step 3: Replace the package imports**

Load `../hello-agents/code/chapter4/llm_client.py` with `importlib.util`, define an empty `MyLLM` subclass of its `HelloAgentsLLM`, and make `first-test.py` import `MyLLM`, `SimpleAgent`, and `CalculatorTool` from local modules.

- [ ] **Step 4: Run all tests and compile checks**

Run: `python -m unittest discover -s tests -v && python -m py_compile my_llm.py simple_agent.py calculator_tool.py first-test.py my_main.py`

Expected: all tests PASS and no compilation output.
