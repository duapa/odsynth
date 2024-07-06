from .abstract_writer import AbstractWriter
from .json_to_disc_writer import JsonToDiscWriter
from .xml_to_disc_writer import XMLToDiscWriter


class WriterFactory:
    _writers = {}

    @classmethod
    def register_writer(cls, writer: type):
        if not issubclass(writer, AbstractWriter):
            raise ValueError("writer must be a subclass of 'AbstractWriter'")

        cls._writers.update({writer.get_name(): writer})

    @classmethod
    def get_writer(cls, writer_name: str, **kwargs) -> AbstractWriter:
        factory_args = {"writer_name"}
        class_kwargs = {k: v for k, v in kwargs.items() if k not in factory_args}

        if writer_name in cls._writers:
            return cls._writers[writer_name](**class_kwargs)

        raise ValueError(f"Specified writer {writer_name} is not supported")

    @classmethod
    def load_writers(cls):
        cls.register_writer(JsonToDiscWriter)
        cls.register_writer(XMLToDiscWriter)


def load_writers():
    WriterFactory.load_writers()
