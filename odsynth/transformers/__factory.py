from typing import Optional

from .abstract_transformer import AbstractTransformer
from .json_transformer import JsonTransformer
from .pandas_transformer import PandasDataframeTransformer
from .xml_transformer import XMLTransformer


class TransformerFactory:
    _transformers = {}

    @classmethod
    def register_transformer(cls, transformer: type):
        if not issubclass(transformer, AbstractTransformer):
            raise ValueError("transformer must be a subclass of 'AbstractTransformer'")

        cls._transformers.update({transformer.get_name(): transformer})

    @classmethod
    def get_transformer(
        cls, transformer_name: str, **kwargs
    ) -> Optional[AbstractTransformer]:
        factory_args = {"transformer_name"}
        class_kwargs = {k: v for k, v in kwargs.items() if k not in factory_args}
        if transformer_name is None:
            return None
        if transformer_name in cls._transformers:
            return cls._transformers[transformer_name](**class_kwargs)

        raise ValueError(f"Specified transformer {transformer_name} is not supported")

    @classmethod
    def load_transformers(cls):
        cls.register_transformer(JsonTransformer)
        cls.register_transformer(PandasDataframeTransformer),
        cls.register_transformer(XMLTransformer)


def load_transformers():
    TransformerFactory.load_transformers()
