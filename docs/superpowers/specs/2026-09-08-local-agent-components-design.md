# Local agent components

## Goal

Run the learning examples without importing the installed `hello-agents` package.

## Components

- `MyLLM` loads and subclasses the Chapter 4 `HelloAgentsLLM` source file. It
  preserves the project's existing `MyLLM()` call site.
- `SimpleAgent` owns an LLM client, name, system prompt, and message history.
  `run(user_prompt)` adds a user message, calls `think(messages)`, records the
  assistant response, and returns it. `get_history()` returns a copy of that
  history.
- `CalculatorTool` exposes a named arithmetic operation. It safely evaluates a
  limited expression grammar rather than using `eval`, and returns a text
  result suitable for an agent.

## Integration

`first-test.py` will import `SimpleAgent`, `CalculatorTool`, and `MyLLM` from
local modules. The calculator remains an optional object until the example
explicitly wires tool use into the agent.

## Verification

Tests will cover local imports, message-history behavior, and calculator
operations without invoking an external LLM API. A compilation/import check
will confirm the scripts no longer require `hello_agents`.
