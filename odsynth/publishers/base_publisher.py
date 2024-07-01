from abc import ABC, abstractmethod


class AbstractPublisher(ABC):
    @abstractmethod
    def publish_data(self):
        raise NotImplementedError("")


class BasePublisher(AbstractPublisher):
    def __init__(
        self,
        schema_spec_file: str,
        plugins_dir: str,
        num_examples: int = 100,
        batch_size: int = 10,
        run_as_daemon: bool = False,
    ):
        self._schema_spec_file = schema_spec_file
        self._num_examples = num_examples
        self._batch_size = batch_size
        self._run_as_daemon = run_as_daemon
        self._plugins_dir = plugins_dir

    def publish_data(self):
        return super().publish_data()
