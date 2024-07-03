from __future__ import annotations

from typing import Any, Dict

from .core import Component, Composite, Plural
from .provider_factory import ProviderFactory
from .transformers import AbstractTransformer
from .utils import load_yaml

PROVIDER_KEY = "provider"
PROVIDER_ARGS_KEY = "provider_args"
SUB_FIELDS_KEY = "fields"
DOM_ROOT_KEY = "$__dom__root"
PLURAL_MAX_COUNT = "max_count"
PLURAL_MARKER = "plural_"


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
    elif SUB_FIELDS_KEY in schema and field_name.startswith(PLURAL_MARKER):
        if PLURAL_MAX_COUNT in schema:
            max_count = convert_max_str_int(schema[PLURAL_MAX_COUNT])
        else:
            max_count = 0
        child_field_name = field_name.split(PLURAL_MARKER)[1]
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
        schema_spec_file: str,
        num_examples: int = 10,
        batch_size: int = 5,
        plugins_dir: str = None,
        transformer: AbstractTransformer = None,
    ) -> None:
        self._schema_spec_file = schema_spec_file
        self._num_examples = num_examples
        self._batch_size = batch_size
        self._user_plugins_dir = plugins_dir
        self._transformer = transformer
        ProviderFactory.load_providers(self._user_plugins_dir)

    def get_data(self):
        schema = load_yaml(self._schema_spec_file)
        data_object_model = generate_dom(DOM_ROOT_KEY, schema)
        data_points = []
        for _ in range(self._num_examples):
            data_points.append(data_object_model.generate_data())
        if self._transformer is None:
            return data_points
        return self._transformer.transform(data_points)

    def yield_data(self):
        schema = load_yaml(self._schema_spec_file)
        data_object_model = generate_dom(DOM_ROOT_KEY, schema)

        num_batches, remainder = divmod(self._num_examples, self._batch_size)
        for _ in range(num_batches):
            data_points = []
            for _ in range(self._batch_size):
                data_points.append(data_object_model.generate_data())
            yield data_points
        if remainder > 0:
            data_points = []
            for _ in range(remainder):
                data_points.append(data_object_model.generate_data())
            yield data_points
