from providers.base_provider import BaseProvider
from providers.claude_provider import ClaudeProvider
from providers.openrouter_provider import OpenRouterProvider


class ProviderFactory:

    _REGISTRY: dict[str, type[BaseProvider]] = {
        "claude": ClaudeProvider,
        "openrouter": OpenRouterProvider,
    }

    @classmethod
    def create(cls, provider_name: str) -> BaseProvider:
        key = provider_name.strip().lower()
        if key not in cls._REGISTRY:
            supported = ", ".join(sorted(cls._REGISTRY))
            raise ValueError(
                f"Unsupported provider: '{provider_name}'. "
                f"Supported providers: {supported}."
            )
        return cls._REGISTRY[key]()
