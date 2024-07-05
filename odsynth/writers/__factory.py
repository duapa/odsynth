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
    def get_writer(cls, writer_name: str, *args, **kwargs):
        if writer_name in cls._writers:
            return cls._writers[writer_name](*args, **kwargs)

        raise ValueError(f"Specified transformer {writer_name} is not supported")

    @classmethod
    def load_writers(cls):
        cls.register_writer(JsonToDiscWriter)
        cls.register_writer(XMLToDiscWriter)


WriterFactory.load_writers()
