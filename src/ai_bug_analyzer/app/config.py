from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")

    project_path: Path = Field(..., alias="BUG_ANALYZER_PROJECT_PATH")
    entry_command: str | None = Field(default=None, alias="BUG_ANALYZER_ENTRY_COMMAND")
    test_command: str | None = Field(default=None, alias="BUG_ANALYZER_TEST_COMMAND")

    max_iterations: int = Field(default=3, alias="BUG_ANALYZER_MAX_ITERATIONS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", populate_by_name=True)
