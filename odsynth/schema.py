from __future__ import annotations

from typing import Any, Dict, List, Optional

from .core import Record
from .formatters import FormatterFactory, load_formatters
from .generator import DataGenerator
from .globals import (
    DOM_ROOT_KEY,
    SCHEMA_ARRAY_TYPE_MARKER,
    SCHEMA_MAX_COUNT_KEY,
    SCHEMA_PROVIDER_ARGS_KEY,
    SCHEMA_PROVIDER_KEY,
    SCHEMA_SUB_FIELDS_KEY,
)
from .providers import ProviderFactory, load_providers
from .publisher import Publisher
from .utils import load_yaml
from .writers import WriterFactory, load_writers

load_providers()
load_formatters()
load_writers()


class SchemaValidationException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ArgumentsParseException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def convert_max_str_int(max_str: str) -> int:
    try:
        max_int = int(max_str)
        return max_int
    except ValueError:
        return 0


def parse_args(data: List[str]) -> Dict[str, str]:
    kwargs = {}
    if not data or data == []:
        return kwargs
    for line in data:
        try:
            key, value = line.split("=")
            kwargs.update({key.replace("-", "_"): value})
        except ValueError:
            raise ArgumentsParseException(f"Invalid key-value pair: {line}")
    return kwargs


class Schema:
    def __init__(self, schema_file: str):
        self._schema = load_yaml(schema_file)
        self.validate()
        self._object_model = self.build_object_model()
        self._generator = None
        self._publisher = None

    def validate(self):
        subfield_err_msg = (
            "A Subfield must either be a Record type or a Primitive Field type"
        )
        if (
            SCHEMA_PROVIDER_KEY not in self._schema
            and SCHEMA_SUB_FIELDS_KEY not in self._schema
        ):
            raise SchemaValidationException(subfield_err_msg)
        if (
            SCHEMA_PROVIDER_KEY in self._schema
            and SCHEMA_SUB_FIELDS_KEY in self._schema
        ):
            raise SchemaValidationException(subfield_err_msg)
        return True

    @classmethod
    def _build_object_model(cls, field_name: str, schema: Dict[str, Any]) -> Record:
        if SCHEMA_PROVIDER_KEY in schema:
            provider_name = schema[SCHEMA_PROVIDER_KEY]
            provider_kwargs = (
                schema[SCHEMA_PROVIDER_ARGS_KEY]
                if SCHEMA_PROVIDER_ARGS_KEY in schema
                else {}
            )
            provider = ProviderFactory.get_provider(
                provider_name, kwargs=provider_kwargs
            )
            provider.field_name = field_name
            return provider
        elif SCHEMA_SUB_FIELDS_KEY in schema:
            max_count = 0
            is_array = False
            if SCHEMA_MAX_COUNT_KEY in schema:
                max_count = convert_max_str_int(schema[SCHEMA_MAX_COUNT_KEY])
            if (
                SCHEMA_ARRAY_TYPE_MARKER in schema
                and schema[SCHEMA_ARRAY_TYPE_MARKER] is True
            ):
                is_array = True

            root = Record(field_name=field_name, max_count=max_count, is_array=is_array)
            for k, v in schema[SCHEMA_SUB_FIELDS_KEY].items():
                root.add(cls._build_object_model(k, v))
            return root

    def build_object_model(self) -> Record:
        return __class__._build_object_model(DOM_ROOT_KEY, self._schema)

    def build_generator(
        self,
        num_examples: int = 10,
        batch_size: int = 10,
        format: str = None,
        formatter_args: Optional[List[str]] = [],
    ) -> Schema:
        parsed_formatter_args = parse_args(formatter_args)
        self._formatter = FormatterFactory.get_formatter(
            format, object_model=self._object_model, **parsed_formatter_args
        )
        self._generator = DataGenerator(
            object_model=self._object_model,
            num_examples=num_examples,
            batch_size=batch_size,
            formatter=self._formatter,
        )

        return self

    def build_publisher(
        self,
        writer: str,
        writer_args: Optional[List[str]],
        num_examples: int = 10,
        batch_size: int = 10,
        format: str = None,
        formatter_args: List[str] = [],
        queue_size: int = 10,
        max_num_workers: int = 2,
        run_as_daemon: bool = False,
    ):
        self.build_generator(
            num_examples=num_examples,
            batch_size=batch_size,
            format=format,
            formatter_args=formatter_args,
        )
        output_writer = WriterFactory.get_writer(
            writer_name=writer, formatter=self.formatter, **parse_args(writer_args)
        )
        self._publisher = Publisher(
            generator=self._generator,
            writer=output_writer,
            queue_size=queue_size,
            max_num_workers=max_num_workers,
            run_as_daemon=run_as_daemon,
        )
        return self

    @property
    def generator(self):
        return self._generator

    @property
    def formatter(self):
        return self._formatter

    def get_data(self):
        return self.generator.get_data()

    def get_data_as_stream(self):
        return self.generator.yield_data()

    def publish_data(self):
        if self._publisher:
            self._publisher.publish_data()
