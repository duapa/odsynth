from __future__ import annotations

from typing import Any, Dict

from .core import Record
from .globals import DOM_ROOT_KEY
from .providers import ProviderFactory, load_providers
from .transformers import TransformerFactory, load_transformers
from .utils import load_yaml

PROVIDER_KEY = "provider"
PROVIDER_ARGS_KEY = "provider_args"
SUB_FIELDS_KEY = "fields"
MAX_COUNT_KEY = "max_count"
ARRAY_TYPE_MARKER = "is_array"


load_providers()
load_transformers()


def convert_max_str_int(max_str: str) -> int:
    try:
        max_int = int(max_str)
        return max_int
    except ValueError:
        return 0


class DataGenerator:
    """Generates data based on a schema specification"""

    def __init__(
        self,
        schema_spec_file: str,
        num_examples: int = 10,
        batch_size: int = 5,
        plugins_dir: str = None,
        transformer_name: str = None,
    ) -> None:
        """Creates a data generator

        Parameters
        -
        schema_spec_file(str): Location of schema specification file (in yaml)
        num_examples (int): Number of examples to be generated
        batch_size (int): Size of batch in which data is to be generated. If the
         batch_size >= num_examples, only one batch will be created.
        plugins_dir (str): Plugins directory from where user's own primitive field providers
         can be loaded
        transformer_name (str): Name of transformer to be used to render the data after generation
        """
        self._schema_spec_file = schema_spec_file
        self._num_examples = num_examples
        self._batch_size = batch_size
        self._user_plugins_dir = plugins_dir
        self._transformer = TransformerFactory.get_transformer(transformer_name)
        self._schema = load_yaml(self._schema_spec_file)
        self._dom = self.build_object_model(DOM_ROOT_KEY, self._schema)

    def build_object_model(self, field_name: str, schema: Dict[str, Any]) -> Record:
        """Creates a Object Model of the schema of a Record or primitive Field."""
        # Validate the schema
        if PROVIDER_KEY not in schema and SUB_FIELDS_KEY not in schema:
            raise ValueError(
                "Subfields must either be a Compound field or a Primitive Fields"
            )
        if PROVIDER_KEY in schema and SUB_FIELDS_KEY in schema:
            raise ValueError(
                "Subfields must either be a Compound field or a Primitive Fields"
            )

        # Generate the DOM
        if PROVIDER_KEY in schema:
            provider_name = schema[PROVIDER_KEY]
            provider_kwargs = (
                schema[PROVIDER_ARGS_KEY] if PROVIDER_ARGS_KEY in schema else {}
            )
            provider = ProviderFactory.get_provider(
                provider_name, kwargs=provider_kwargs
            )
            provider.field_name = field_name
            return provider
        elif SUB_FIELDS_KEY in schema:
            max_count = 0
            is_array = False
            if MAX_COUNT_KEY in schema:
                max_count = convert_max_str_int(schema[MAX_COUNT_KEY])
            if ARRAY_TYPE_MARKER in schema and schema[ARRAY_TYPE_MARKER] is True:
                is_array = True

            root = Record(field_name=field_name, max_count=max_count, is_array=is_array)
            for k, v in schema[SUB_FIELDS_KEY].items():
                root.add(self.build_object_model(k, v))
            return root

    def get_data(self):
        """Generate samples of data using the specified schema"""
        data_points = []
        for _ in range(self._num_examples):
            data_points.append(self._dom.generate_data())
        if self._transformer is None:
            return data_points
        return self._transformer.transform(data_points)

    def yield_data(self):
        """Yeild 'self._batch_size samples' of data using the specified
        schema until the specified number of examples have all been generated."""
        num_batches, remainder = divmod(self._num_examples, self._batch_size)
        for _ in range(num_batches):
            data_points = []
            for _ in range(self._batch_size):
                data_points.append(self._dom.generate_data())
            yield data_points
        if remainder > 0:
            data_points = []
            for _ in range(remainder):
                data_points.append(self._dom.generate_data())
            yield data_points
