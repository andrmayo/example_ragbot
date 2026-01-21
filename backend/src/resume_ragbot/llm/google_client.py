from google import genai
from google.genai import types

from resume_ragbot.config import settings
from resume_ragbot.llm.base import LLMClient, LLMResponse, InputMessage


class GoogleClient(LLMClient):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.google_api_key
        self.model = model or settings.google_model
        self.client = genai.Client(api_key=self.api_key)

    def _convert_messages(self, messages: list[InputMessage]) -> list[types.Content]:
        return [
            types.Content(
                role="user" if m.role == "user" else "model",
                parts=[types.Part(text=m.content)],
            )
            for m in messages
        ]

    def complete(
        self,
        messages: list[InputMessage],
        temperature: float = settings.default_temp,
        system: str | None = None,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            system_instruction=system,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=self._convert_messages(messages),
            config=config,
        )

        text = response.text or ""
        usage = response.usage_metadata

        return LLMResponse(
            content=text,
            model=self.model,
            input_tokens=usage.prompt_token_count if usage else None,
            output_tokens=usage.candidates_token_count if usage else None,
        )

    async def complete_async(
        self,
        messages: list[InputMessage],
        temperature: float = settings.default_temp,
        system: str | None = None,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            system_instruction=system,
        )

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=self._convert_messages(messages),
            config=config,
        )

        text = response.text or ""
        usage = response.usage_metadata

        return LLMResponse(
            content=text,
            model=self.model,
            input_tokens=usage.prompt_token_count if usage else None,
            output_tokens=usage.candidates_token_count if usage else None,
        )
