import openai
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from resume_ragbot.config import settings
from resume_ragbot.llm.base import LLMClient, LLMResponse, InputMessage


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model
        self.client = openai.OpenAI(api_key=self.api_key)
        self.async_client = openai.AsyncOpenAI(api_key=self.api_key)

    def _convert_messages(
        self,
        messages: list[InputMessage],
        system: str | None = None,
    ) -> list[ChatCompletionMessageParam]:
        result: list[ChatCompletionMessageParam] = []
        if system:
            result.append(
                ChatCompletionSystemMessageParam(role="system", content=system)
            )
        for m in messages:
            if m.role == "user":
                result.append(
                    ChatCompletionUserMessageParam(role=m.role, content=m.content)
                )
            elif m.role == "assistant":
                result.append(
                    ChatCompletionAssistantMessageParam(
                        role="assistant", content=m.content
                    )
                )
            else:
                raise ValueError(f"Unknown role: {m.role}")

        return result

    def complete(
        self,
        messages: list[InputMessage],
        temperature: float = settings.default_temp,
        system: str | None = None,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self._convert_messages(messages, system),
            max_tokens=max_tokens,
            temperature=temperature,
        )

        choice = response.choices[0]
        text = choice.message.content or ""

        return LLMResponse(
            content=text,
            model=response.model,
            input_tokens=response.usage.prompt_tokens if response.usage else None,
            output_tokens=response.usage.completion_tokens if response.usage else None,
        )

    async def complete_async(
        self,
        messages: list[InputMessage],
        temperature: float = settings.default_temp,
        system: str | None = None,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=self._convert_messages(messages, system),
            max_tokens=max_tokens,
            temperature=temperature,
        )
        choice = response.choices[0]
        text = choice.message.content or ""

        return LLMResponse(
            content=text,
            model=response.model,
            input_tokens=response.usage.prompt_tokens if response.usage else None,
            output_tokens=response.usage.completion_tokens if response.usage else None,
        )
