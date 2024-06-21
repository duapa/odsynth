from .providers.simple_text import Text, FirstName, LastName
from .providers.random_int import RandomInt
from ..core import Primitive
from typing import Dict

class PrimitivesFactory():
    def __init__(self):
        self._primitives: Dict[str, Primitive] = {}
    
    def register_provider(self,provider_name: str, provider: Primitive):
        if provider_name in self._primitives:
            raise ValueError(f"Specified provider already exists. Provider Name: {provider_name}")
        self._primitives.update({provider_name: provider})

    def get_provider(self, provider_name: str, provider_kwargs: dict = {}) -> Primitive:
        if provider_name in self._primitives:
            provider = self._primitives[provider_name]
            provider.provider_kwargs = provider_kwargs
            return provider
        raise ValueError(f"Specified provider {provider_name} is not supported")
    

def build_primitives_factory():
    factory = PrimitivesFactory()
    factory.register_provider(Text.get_provider_name(), Text())
    factory.register_provider(FirstName.get_provider_name(), FirstName())
    factory.register_provider(LastName.get_provider_name(), LastName())
    factory.register_provider(RandomInt.get_provider_name(), RandomInt())

    return factory