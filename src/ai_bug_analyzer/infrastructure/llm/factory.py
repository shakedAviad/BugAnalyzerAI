from __future__ import annotations

import os

from langchain_openai import ChatOpenAI

DEFAULT_MODEL: str = "gpt-4.1-mini"


def create_chat_model(model: str | None = None) -> ChatOpenAI:

    selected_model: str = model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL

    return ChatOpenAI(model=selected_model, api_key=os.getenv("OPENAI_API_KEY"))
