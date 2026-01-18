from typing import cast

from resume_ragbot.config import LLMProvider, settings
from resume_ragbot.llm.anthropic_client import AnthropicClient
from resume_ragbot.llm.base import LLMClient
from resume_ragbot.llm.google_client import GoogleClient
from resume_ragbot.llm.openai_client import OpenAIClient


def get_client(
    provider: LLMProvider | str | None = None,
    model: str | None = None,
) -> LLMClient:
    provider = cast(LLMProvider | str, provider or settings.default_llm_provider)

    if provider == "anthropic":
        return AnthropicClient(model=model)
    elif provider == "openai":
        return OpenAIClient(model=model)
    elif provider == "google":
        return GoogleClient(model=model)
    else:
        raise ValueError(f"Unknown provider: {provider}")
