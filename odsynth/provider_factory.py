from typing import Any, Dict

from .core import Provider
from .plugins_loader import load_plugins
from .providers import FirstName, LastName, RandomInt, Text


class ProviderFactory:
    _providers = {}

    @classmethod
    def register_provider(cls, provider_name: str, provider: Provider):
        if provider_name in cls._providers:
            raise ValueError(
                f"Specified provider already exists. Provider Name: {provider_name}"
            )
        cls._providers.update({provider_name: provider})

    @classmethod
    def get_provider(
        cls, provider_name: str, provider_kwargs: Dict[str, Any] = {}
    ) -> Provider:
        if provider_name in cls._providers:
            provider = cls._providers[provider_name]
            provider.provider_kwargs = provider_kwargs
            return provider
        raise ValueError(f"Specified provider {provider_name} is not supported")

    @classmethod
    def load_providers(cls, plugins_dir: str = None):
        cls.register_provider(FirstName.get_provider_name(), FirstName())
        cls.register_provider(LastName.get_provider_name(), LastName())
        cls.register_provider(RandomInt.get_provider_name(), RandomInt())
        cls.register_provider(Text.get_provider_name(), Text())

        if plugins_dir:
            load_plugins(plugin_folder_name=plugins_dir)
