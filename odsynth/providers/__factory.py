from typing import Any, Dict

from ..core import Provider
from ..plugins_loader import load_plugins
from .random_int import RandomInt
from .simple_text import FirstName, LastName, Text
from ..globals import get_providers_home


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
        cls, provider_name: str, *args, **kwargs
    ) -> Provider:
        if provider_name in cls._providers:
            provider = cls._providers[provider_name](*args, **kwargs)
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


ProviderFactory.load_providers(get_providers_home())
