from typing import List, Optional

import typer

from ..schema import Schema

app = typer.Typer()


@app.command()
def publish_data(
    schema_spec_file: str = typer.Option(
        help="Location of schema definition for data generation"
    ),
    num_samples: int = typer.Option(10, help="Number of samples to be generated"),
    batch_size: int = typer.Option(
        10, help="Number of examples to be generated in a batch"
    ),
    run_as_daemon: bool = typer.Option(
        False, "--run-as-daemon", "-d", help="Run in infinite loop"
    ),
    max_num_workers: int = typer.Option(
        2,
        help="Maximum number of threads created when writing data",
    ),
    queue_size: int = typer.Option(
        10,
        help="Size of the queue for thread pool when writing data",
    ),
    writer: str = typer.Option(
        "local_disc",
        help="Writer to use for publishing the data",
    ),
    writer_arg: Optional[List[str]] = typer.Option(
        None, help="Arguments needed by the writer"
    ),
    format: Optional[str] = typer.Option(
        "json", help="Format in which data is generated (xml, json, text, etc)"
    ),
    formatter_arg: Optional[List[str]] = typer.Option(None, help="Formatter arguments"),
):
    schema = Schema(schema_file=schema_spec_file).build_publisher(
        writer=writer,
        writer_args=writer_arg,
        num_examples=num_samples,
        batch_size=batch_size,
        format=format,
        formatter_args=formatter_arg,
        queue_size=queue_size,
        max_num_workers=max_num_workers,
        run_as_daemon=run_as_daemon,
    )
    schema.publish_data()


def main():
    app()
