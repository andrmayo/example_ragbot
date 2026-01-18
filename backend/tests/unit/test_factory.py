from resume_ragbot.llm import get_client
from resume_ragbot.llm.anthropic_client import AnthropicClient
from resume_ragbot.llm.openai_client import OpenAIClient
from resume_ragbot.llm.google_client import GoogleClient


def test_get_client_anthropic():
    client = get_client(provider="anthropic")
    assert isinstance(client, AnthropicClient)


def test_get_client_openai():
    client = get_client(provider="openai")
    assert isinstance(client, OpenAIClient)


def test_get_client_google():
    client = get_client(provider="google")
    assert isinstance(client, GoogleClient)


def test_get_client_custom_model():
    client = get_client(provider="anthropic", model="claude-haiku-3-5-20241022")
    assert client.model == "claude-haiku-3-5-20241022"
