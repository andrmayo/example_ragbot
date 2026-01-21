from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

from resume_ragbot.config import settings

roles = Literal["user", "assistant"]


@dataclass
class InputMessage:
    role: roles
    content: str


@dataclass
class LLMResponse:
    content: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None


class LLMClient(ABC):
    model: str

    @abstractmethod
    def complete(
        self,
        messages: list[InputMessage],
        temperature: float = settings.default_temp,
        system: str | None = None,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        """Generate a complete from a list of messages."""
        ...

    @abstractmethod
    async def complete_async(
        self,
        messages: list[InputMessage],
        temperature: float,
        system: str | None = None,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        """Async version of complete."""
        ...
