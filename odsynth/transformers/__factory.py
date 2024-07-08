from typing import Optional

from .abstract_transformer import AbstractTransformer
from .json_transformer import JsonTransformer
from .pandas_transformer import PandasDataframeTransformer
from .xml_transformer import XMLTransformer


class TransformerFactory:
    """Implements a strategy for choosing between
    various implementations of data transformers"""

    _transformers = {}

    @classmethod
    def register_transformer(cls, transformer: type):
        """Register a data tranformer"""
        if not issubclass(transformer, AbstractTransformer):
            raise ValueError("transformer must be a subclass of 'AbstractTransformer'")

        cls._transformers.update({transformer.get_name(): transformer})

    @classmethod
    def get_transformer(
        cls, transformer_name: str, **kwargs
    ) -> Optional[AbstractTransformer]:
        """Gets a data transformer

        Parameters:
        -----------
        transformer_name (str): Identifying name of the data transformer

        Returns:
        ------
        transformer (AbstractTransformer): Transformer to be used for in memory data
        transformations
        """
        factory_args = {"transformer_name"}
        class_kwargs = {k: v for k, v in kwargs.items() if k not in factory_args}
        if transformer_name is None:
            return None
        if transformer_name in cls._transformers:
            return cls._transformers[transformer_name](**class_kwargs)

        raise ValueError(f"Specified transformer {transformer_name} is not supported")

    @classmethod
    def load_transformers(cls):
        """Registers transformer types and makes them available for creating new transformers"""
        cls.register_transformer(JsonTransformer)
        cls.register_transformer(PandasDataframeTransformer),
        cls.register_transformer(XMLTransformer)


def load_transformers():
    TransformerFactory.load_transformers()
