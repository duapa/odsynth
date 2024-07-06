import concurrent.futures
import threading
from queue import Queue
from typing import Any, Dict, List

from .generator import DataGenerator
from .writers import AbstractWriter, load_writers

load_writers()


class Publisher:
    def __init__(
        self,
        schema_spec_file: str,
        plugins_dir: str,
        writer: AbstractWriter,
        num_examples: int = 100,
        batch_size: int = 10,
        queue_size: int = 10,
        max_num_workers: int = 5,
        run_as_daemon: bool = False,
    ):
        self._schema_spec_file = schema_spec_file
        self._plugins_dir = plugins_dir
        self._num_examples = num_examples
        self._batch_size = batch_size
        self._run_as_daemon = run_as_daemon
        self._processing_queue = Queue(maxsize=queue_size)
        self._max_num_workers = max_num_workers
        self._writer_shutdown_event = threading.Event()
        self._writer = writer

        if self._run_as_daemon:
            self._generator = DataGenerator(
                schema_spec_file=self._schema_spec_file,
                plugins_dir=self._plugins_dir,
                num_examples=self._batch_size,
                batch_size=self._batch_size,
            )
        else:
            self._generator = DataGenerator(
                schema_spec_file=self._schema_spec_file,
                plugins_dir=self._plugins_dir,
                num_examples=self._num_examples,
                batch_size=self._batch_size,
            )

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
