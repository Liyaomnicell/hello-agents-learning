"""A minimal conversation agent for the local learning examples."""


class SimpleAgent:
    """Combines a system prompt, message history, and an LLM client."""

    def __init__(self, name, llm, system_prompt):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self._history = []

    def run(self, user_prompt):
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self._history,
            {"role": "user", "content": user_prompt},
        ]
        response = self.llm.think(messages) or ""
        self._history.extend((
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": response},
        ))
        return response

    def get_history(self):
        """Return a shallow copy of the stored user/assistant messages."""
        return list(self._history)
