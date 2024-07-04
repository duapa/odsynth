from typing import Any, Dict

from ..core import Provider
from ..plugins_loader import load_plugins
from . import FirstName, LastName, RandomInt, Text


class ProviderFactory:
    _providers = {}

    @classmethod
    def register_provider(cls, provider: Provider):
        provider_name = provider.get_provider_name()
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
            provider = cls._providers[provider_name]()
            provider.provider_kwargs = provider_kwargs
            return provider
        raise ValueError(f"Specified provider {provider_name} is not supported")

    @classmethod
    def load_providers(cls, plugins_dir: str = None):
        cls.register_provider(FirstName)
        cls.register_provider(LastName)
        cls.register_provider(RandomInt)
        cls.register_provider(Text)

        if plugins_dir:
            load_plugins(plugin_folder_name=plugins_dir)
