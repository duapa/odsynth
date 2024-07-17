import concurrent.futures
import threading
from queue import Queue
from typing import Any, Dict, List

from .generator import DataGenerator
from .writers import AbstractWriter


class WriterArgumentsException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Publisher:
    """Publishes data from a data generator to a specified medium"""

    def __init__(
        self,
        generator: DataGenerator,
        writer: AbstractWriter,
        queue_size: int = 10,
        max_num_workers: int = 2,
        run_as_daemon: bool = False,
    ):
        """
        Creates a data publisher for generating and persisting data
         according to a schem specification

        Parameters
        -
        writer(AbstractWriter): A writer for persisting the generated data
        num_examples (int): number of records to be generated
        batch_size (int): Size of batch in which data is to be generated. If the
         batch_size >= num_examples, only one batch will be created.
        queue_size (int): Data batches are written using worker threads. Queue Size
         dictates the size of the queue for worker threads which write the data
        max_num_workers (int): The maximum number of worker threads to use when
         publishing data to a medium.
        run_as_daemon (bool): Run the publisher in an unending loop? True == yes :)

        """

        self._run_as_daemon = run_as_daemon
        self._processing_queue = Queue(maxsize=queue_size)
        self._max_num_workers = max_num_workers
        self._writer_shutdown_event = threading.Event()

        self._writer = writer
        self._generator = generator
        if self._run_as_daemon:
            self._generator.num_examples = self._generator.batch_size

    def publish_data(self):
        def write_batch(batch: List[Dict[str, Any]]):
            self._writer.write_data(batch)

        def producer():
            def add_to_queue():
                for batch in self._generator.yield_data():
                    self._processing_queue.put(batch)

            while not self._writer_shutdown_event.is_set():
                add_to_queue()
                if not self._run_as_daemon:
                    self._writer_shutdown_event.set()

        def consumer():
            while (not self._writer_shutdown_event.is_set()) or (
                not self._processing_queue.empty()
            ):
                batch = self._processing_queue.get()
                write_batch(batch)

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self._max_num_workers
        ) as executor:
            executor.submit(consumer)
            executor.submit(producer)
