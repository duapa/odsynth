from .providers.simple_text import Text, FirstName, LastName
from .providers.random_int import RandomInt
from ..core import Primitive
from typing import Dict, Any


primitives: Dict[str, Primitive] = {}

def register_provider(provider_name: str, provider: Primitive):
    if provider_name in primitives:
        raise ValueError(f"Specified provider already exists. Provider Name: {provider_name}")
    primitives.update({provider_name: provider})

def get_provider(provider_name: str, provider_kwargs: Dict[str, Any] = {}) -> Primitive:
    if provider_name in primitives:
        provider = primitives[provider_name]
        provider.provider_kwargs = provider_kwargs
        return provider
    raise ValueError(f"Specified provider {provider_name} is not supported")

def build_primitives_factory():
    register_provider(Text.get_provider_name(), Text())
    register_provider(FirstName.get_provider_name(), FirstName())
    register_provider(LastName.get_provider_name(), LastName())
    register_provider(RandomInt.get_provider_name(), RandomInt())