import os

import anthropic

from providers.base_provider import BaseProvider


class ClaudeProvider(BaseProvider):

    DEFAULT_MODEL = "claude-sonnet-4-6"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. "
                "Please configure it in your .env file."
            )
        self._client = anthropic.Anthropic(api_key=key)
        self._model = model or self.DEFAULT_MODEL

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        kwargs: dict = {
            "model": self._model,
            "max_tokens": 8096,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        message = self._client.messages.create(**kwargs)
        if not message.content:
            raise RuntimeError(
                "Claude returned an empty response. "
                "The request may have been filtered or exceeded the token limit."
            )
        return message.content[0].text
