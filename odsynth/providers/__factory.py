from ..core import Field
from ..globals import get_providers_home
from ..plugins_loader import load_plugins
from .faker import FakerField


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
        elif provider_name.startswith("faker"):
            # TODO: Validate faker's provider name
            faker_type = provider_name.split(".")[1]
            provider = FakerField(faker_type=faker_type, **class_kwargs)
            return provider
        raise ValueError(
            f"Specified primitive field provider {provider_name} is not supported"
        )

    @classmethod
    def load_providers(cls, plugins_dir: str = None):
        """Registers the various provider types and makes them available
        for synthesizing data"""
        cls.register_provider(FakerField)

        if plugins_dir:
            load_plugins(plugin_folder_name=plugins_dir)


def load_providers():
    ProviderFactory.load_providers(get_providers_home())
