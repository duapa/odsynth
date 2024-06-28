from typing import Any, Dict

from .core import Primitive
from .plugins_loader import load_plugins
from .providers import FirstName, LastName, RandomInt

providers: Dict[str, Primitive] = {}


def register_provider(provider_name: str, provider: Primitive):
    if provider_name in providers:
        raise ValueError(
            f"Specified provider already exists. Provider Name: {provider_name}"
        )
    providers.update({provider_name: provider})


def get_provider(provider_name: str, provider_kwargs: Dict[str, Any] = {}) -> Primitive:
    if provider_name in providers:
        provider = providers[provider_name]
        provider.provider_kwargs = provider_kwargs
        return provider
    raise ValueError(f"Specified provider {provider_name} is not supported")


def build_primitives_factory(plugins_dir: str = None):
    register_provider(FirstName.get_provider_name(), FirstName())
    register_provider(LastName.get_provider_name(), LastName())
    register_provider(RandomInt.get_provider_name(), RandomInt())

    if plugins_dir:
        load_plugins(plugin_folder_name=plugins_dir)
