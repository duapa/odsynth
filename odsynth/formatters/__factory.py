from typing import Optional

from .abstract_formatter import AbstractFormatter
from .base_formatter import BaseFormatter
from .delimited_text_formatter import DelimitedTextFormatter
from .json_formatter import JsonFormatter
from .pandas_formatter import PandasDataframeFormatter
from .xml_formatter import XMLFormatter


class FormatterFactory:
    """Implements a strategy for choosing between
    various implementations of data formatters"""

    _formatters = {}

    @classmethod
    def register_formatter(cls, formatter: type):
        """Register a data formatter"""
        if not issubclass(formatter, AbstractFormatter):
            raise ValueError("Formatter must be a subclass of 'AbstractFormatter'")

        cls._formatters.update({formatter.get_name(): formatter})

    @classmethod
    def get_formatter(
        cls, formatter_name: str, **kwargs
    ) -> Optional[AbstractFormatter]:
        """Gets a data formatter

        Parameters:
        -----------
        formatter_nname (str): Identifying name of the data formatter

        Returns:
        ------
        formatter (AbstractFormatter): Formatter to be used for in memory data
        transformations
        """
        factory_args = {"formatter_name"}
        class_kwargs = {k: v for k, v in kwargs.items() if k not in factory_args}
        if formatter_name in cls._formatters:
            return cls._formatters[formatter_name](**class_kwargs)
        return BaseFormatter(**class_kwargs)

    @classmethod
    def load_formatters(cls):
        """Registers formatter types"""
        cls.register_formatter(JsonFormatter)
        cls.register_formatter(PandasDataframeFormatter),
        cls.register_formatter(XMLFormatter)
        cls.register_formatter(DelimitedTextFormatter)


def load_formatters():
    FormatterFactory.load_formatters()
