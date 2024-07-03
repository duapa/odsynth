import typer
from typing_extensions import Annotated

from odsynth.publisher import Publisher
from odsynth.writers import JsonToDiscWriter

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
        help="Location on disk where json data will be stored"
    ),
    run_as_daemon: bool = typer.Option(
        False, "--run-as-daemon", "-d", help="Run in infinite loop"
    ),
    plugins_dir: str = typer.Option(
        None, help="Location for user added data generation providers."
    ),
):
    publisher = Publisher(
        schema_spec_file=schema_spec_file,
        plugins_dir=plugins_dir,
        num_examples=num_samples,
        batch_size=batch_size,
        run_as_daemon=run_as_daemon,
        writer=JsonToDiscWriter(base_dir=output_dir),
    )
    publisher.publish_data()


if __name__ == "__main__":
    app()
