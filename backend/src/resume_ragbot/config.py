from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LLMProvider = Literal["anthropic", "openai", "google"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None
    google_api_key: str | None = None
    default_llm_provider: LLMProvider = "anthropic"
    anthropic_model: str = "claude-sonnet-4-20250514"
    openai_model: str = "gpt-4o"
    google_model: str = "gemini-2.0-flash"
    default_temp: float = Field(default=0.7, ge=0, le=2)
    default_embedding_model: str = "all-MiniLM-L6-v2"


# NOTE: "all-MiniLM-L6-v2" for sentence_transformer, good balance between speed and quality


settings = Settings()
