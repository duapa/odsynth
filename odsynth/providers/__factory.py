from ..core import Field
from ..globals import get_providers_home
from ..plugins_loader import load_plugins
from .random_int import RandomInt
from .simple_text import FirstName, LastName, Text
from .ssn import SSN


class ProviderFactory:
    """Creates implementations of various primitive field providers"""

    _providers = {}

    @classmethod
    def register_provider(cls, provider: Field):
        """Register a data provider"""
        provider_name = provider.get_name()
        if provider_name in cls._providers:
            raise ValueError(
                f"Specified provider already exists. Provider Name: {provider_name}"
            )
        cls._providers.update({provider_name: provider})

    @classmethod
    def get_provider(cls, provider_name: str, **kwargs) -> Field:
        """Gets a data provider

        Parameters:
        -----------
        provider_name (str): Identifying name of the primitive field provider

        Returns:
        ------
        provider (Field): A primitive data generator
        """
        factory_args = {"provider_name"}
        class_kwargs = {k: v for k, v in kwargs.items() if k not in factory_args}
        if provider_name in cls._providers:
            provider = cls._providers[provider_name](**class_kwargs)
            return provider
        raise ValueError(
            f"Specified primitive field provider {provider_name} is not supported"
        )

    @classmethod
    def load_providers(cls, plugins_dir: str = None):
        """Registers the various provider types and makes them available
        for synthesizing data"""
        cls.register_provider(FirstName)
        cls.register_provider(LastName)
        cls.register_provider(RandomInt)
        cls.register_provider(Text)
        cls.register_provider(SSN)

        if plugins_dir:
            load_plugins(plugin_folder_name=plugins_dir)


def load_providers():
    ProviderFactory.load_providers(get_providers_home())
