from __future__ import annotations

from typing import Any, Dict

from .core import Component, Composite, Plural
from .plugins_loader import load_plugins
from .provider_factory import ProviderFactory
from .utils import load_yaml
from .transformers import BaseTransformer

PROVIDER_KEY = "provider"
PROVIDER_ARGS_KEY = "provider_args"
SUB_FIELDS_KEY = "fields"
DOM_ROOT_KEY = "$__dom__root"
PLURAL_MAX_COUNT = "max_count"


def convert_max_str_int(max_str: str) -> int:
    try:
        max_int = int(max_str)
        return max_int
    except ValueError:
        return 0


def generate_dom(field_name: str, schema: Dict[str, Any]) -> Component:
    if field_name == DOM_ROOT_KEY:
        root = Composite(DOM_ROOT_KEY)
        for k, v in schema.items():
            root.add(generate_dom(k, v))
        return root
    elif PROVIDER_KEY in schema:
        provider_name = schema[PROVIDER_KEY]
        args = schema[PROVIDER_ARGS_KEY] if PROVIDER_ARGS_KEY in schema else {}
        provider = ProviderFactory.get_provider(provider_name, args)
        provider.field_name = field_name
        return provider
    elif SUB_FIELDS_KEY in schema and field_name.startswith("plural_"):
        if PLURAL_MAX_COUNT in schema:
            max_count = convert_max_str_int(schema[PLURAL_MAX_COUNT])
        else:
            max_count = 0
        child_field_name = field_name.split("plural_")[1]
        root = Plural(field_name=child_field_name, max_count=max_count)
        for k, v in schema[SUB_FIELDS_KEY].items():
            root.add(generate_dom(k, v))
        return root
    elif SUB_FIELDS_KEY in schema:
        root = Composite(field_name)
        for k, v in schema[SUB_FIELDS_KEY].items():
            root.add(generate_dom(k, v))
        return root
    

class DataGenerator:
    def __init__(
            self,
            schema: Dict[str, Any],
            num_examples:int=10, 
            plugins_dir:str=None,
            transformer: BaseTransformer = None
        ) -> None:
        self._schema = schema
        self._num_examples= num_examples
        self._user_plugins_dir = plugins_dir
        self._transformer = transformer
        ProviderFactory.load_providers(self._user_plugins_dir)

    def get_data(self):
        data_object_model = generate_dom(DOM_ROOT_KEY, schema=self._schema)
        data_points = []
        for _ in range(self._num_examples):
            data_points.append(data_object_model.generate_data())
        if self._transformer is None:
            return data_points
        return self._transformer.transform(data_points)
    
    def yield_data(self):
        data_object_model = generate_dom(DOM_ROOT_KEY, schema=self._schema)
        for _ in range(self._num_examples):
            yield data_object_model.generate_data()


