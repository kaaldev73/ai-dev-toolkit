from config.config import DEFAULT_PROVIDER
from providers.provider_factory import ProviderFactory


class AITaskService:

    def __init__(self, provider_name: str | None = None) -> None:
        name = provider_name or DEFAULT_PROVIDER
        self._provider = ProviderFactory.create(name)

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        return self._provider.generate(prompt, system_prompt)
