from .abstract_writer import AbstractWriter
from .disc_writer import DiscWriter


class WriterFactory:
    """Implements a strategy for choosing between
    various implementations of data writers"""

    _writers = {}

    @classmethod
    def register_writer(cls, writer: type):
        """Register a data writer"""
        if not issubclass(writer, AbstractWriter):
            raise ValueError("writer must be a subclass of 'AbstractWriter'")

        cls._writers.update({writer.get_name(): writer})

    @classmethod
    def get_writer(cls, writer_name: str, **kwargs) -> AbstractWriter:
        """Gets a data writer

        Parameters:
        -----------
        writer_name (str): Identifying name of the data writer

        Returns:
        ------
        writer (AbstractWriter): Writer to be used for persisting data
        """
        factory_args = {"writer_name"}
        class_kwargs = {k: v for k, v in kwargs.items() if k not in factory_args}

        if writer_name in cls._writers:
            return cls._writers[writer_name](**class_kwargs)

        raise ValueError(f"Specified writer {writer_name} is not supported")

    @classmethod
    def load_writers(cls):
        """Registers the various writer types and makes them available
        for creating new writers"""
        cls.register_writer(DiscWriter)


def load_writers():
    WriterFactory.load_writers()
