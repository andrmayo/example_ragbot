from typing import Any

import anthropic

from resume_ragbot.config import settings
from resume_ragbot.llm.base import LLMClient, LLMResponse, Message


class AnthropicClient(LLMClient):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        # using 'or' here handles falsy values being passed in as api_key
        self.api_key = api_key or settings.anthropic_api_key
        self.model = model or settings.anthropic_model
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.async_client = anthropic.AsyncAnthropic(api_key=self.api_key)

    def _convert_messages(
        self, messages: list[Message]
    ) -> list[anthropic.types.MessageParam]:
        return [{"role": m.role, "content": m.content} for m in messages]

    def complete(
        self,
        messages: list[Message],
        temperature: float = settings.default_temp,
        system: str | None = None,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": self._convert_messages(messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system:
            kwargs["system"] = system

        response = self.client.messages.create(**kwargs)
        text = ""
        if response.content and response.content[0].type == "text":
            text = response.content[0].text

        return LLMResponse(
            content=text,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

    async def complete_async(
        self,
        messages: list[Message],
        temperature: float = settings.default_temp,
        system: str | None = None,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": self._convert_messages(messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system:
            kwargs["system"] = system

        response = await self.async_client.messages.create(**kwargs)
        text = ""
        if response.content and response.content[0].type == "text":
            text = response.content[0].text

        return LLMResponse(
            content=text,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )
