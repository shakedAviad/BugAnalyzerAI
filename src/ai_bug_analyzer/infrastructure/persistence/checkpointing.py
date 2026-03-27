from __future__ import annotations

from langgraph.checkpoint.memory import InMemorySaver


def create_in_memory_checkpointer() -> InMemorySaver:
    return InMemorySaver()
