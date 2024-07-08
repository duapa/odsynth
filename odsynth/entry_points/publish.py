from typing import Dict, List, Optional

import typer

from ..publisher import Publisher
from ..writers import WriterFactory

app = typer.Typer()


def get_writer_kwargs(data: List[str]) -> Dict[str, str]:
    kwargs = {}
    if not data:
        return kwargs
    for line in data:
        try:
            key, value = line.split("=")
            kwargs.update({key.replace("-", "_"): value})
        except ValueError:
            typer.echo(f"Invalid key-value pair: {line}")
    return kwargs


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
    writer: str = typer.Option(
        "json_to_disc",
        help="Writer to use for publishing the data",
    ),
    writer_arg: Optional[List[str]] = typer.Option(
        None, help="Keyword Arguments needed by the writer"
    ),
):
    writer_kwargs = get_writer_kwargs(writer_arg)
    data_writer = WriterFactory.get_writer(writer_name=writer, **writer_kwargs)

    publisher = Publisher(
        schema_spec_file=schema_spec_file,
        plugins_dir=plugins_dir,
        num_examples=num_samples,
        batch_size=batch_size,
        run_as_daemon=run_as_daemon,
        writer=data_writer,
        max_num_workers=max_num_workers,
        queue_size=queue_size,
    )
    publisher.publish_data()


def main():
    app()
