import os
import time

import typer

from odsynth.globals import DEFAULT_OUTPUT_SUBDIR
from odsynth.publisher import Publisher
from odsynth.writers import WriterFactory

app = typer.Typer()


@app.command()
def publish_data(
    schema_spec_file: str = typer.Option(
        help="Location of schema definition for data generation"
    ),
    num_samples: int = typer.Option(help="Number of samples to be generated"),
    batch_size: int = typer.Option(
        help="Number of examples to be generated in a batch"
    ),
    output_dir: str = typer.Option(
        None, help="Location on disk where json data will be stored"
    ),
    run_as_daemon: bool = typer.Option(
        False, "--run-as-daemon", "-d", help="Run in infinite loop"
    ),
    plugins_dir: str = typer.Option(
        None, help="Location for user added data generation providers."
    ),
    max_num_workers: int = typer.Option(
        2,
        help="Maximum number of threads created when writing data",
    ),
    queue_size: int = typer.Option(
        10,
        help="Size of the queue for thread pool when writing data",
    ),
):
    timestamp = int(time.time() * 1e6)
    if output_dir is None:
        _output_dir = f"{os.getcwd()}/{DEFAULT_OUTPUT_SUBDIR}/xml/{timestamp}"
    else:
        _output_dir = f"{output_dir}/xml/{timestamp}"

    publisher = Publisher(
        schema_spec_file=schema_spec_file,
        plugins_dir=plugins_dir,
        num_examples=num_samples,
        batch_size=batch_size,
        run_as_daemon=run_as_daemon,
        writer=WriterFactory.get_writer(
            writer_name="xml_to_disc", base_dir=_output_dir
        ),
        max_num_workers=max_num_workers,
        queue_size=queue_size,
    )
    publisher.publish_data()


if __name__ == "__main__":
    app()
