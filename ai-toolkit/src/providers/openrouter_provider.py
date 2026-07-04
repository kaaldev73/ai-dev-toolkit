import os

import requests

from providers.base_provider import BaseProvider


class OpenRouterProvider(BaseProvider):

    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    DEFAULT_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set. "
                "Please configure it in your .env file."
            )
        self._api_key = key
        self._model = model or self.DEFAULT_MODEL

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = requests.post(
            self.API_URL,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self._model,
                "messages": messages,
            },
            timeout=60,
        )
        response.raise_for_status()

        body = response.json()
        if "error" in body:
            raise RuntimeError(
                f"OpenRouter API error: {body['error'].get('message', body['error'])}"
            )
        choices = body.get("choices")
        if not choices:
            raise RuntimeError(
                "OpenRouter returned an empty response (no choices). "
                "The model may be unavailable or rate-limited."
            )
        return choices[0]["message"]["content"]
