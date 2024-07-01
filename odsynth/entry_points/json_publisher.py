import typer
from typing_extensions import Annotated

from odsynth.publishers.json_publisher import JsonPublisher

app = typer.Typer()

@app.command()
def publish_data(
    schema_spec_file: Annotated[
        str, typer.Option(help="Location of schema definition for data generation")
    ],
    num_samples: Annotated[int, typer.Option(help="Number of samples to be generated")],
    batch_size: Annotated[int, typer.Option(help="Number of examples to be generated in a batch")],
    output_dir: Annotated[str, typer.Option(help="Location on disk where json data will be stored")],
    run_as_daemon: Annotated[int, typer.Option(help="Run in infinite loop")],
    plugins_dir: Annotated[
        str, typer.Option(help="Location for user added data generation providers.")
    ] = None,
    
):
    as_daemon = False
    if run_as_daemon == 1:
        as_daemon=True
    publisher = JsonPublisher(
        schema_file=schema_spec_file,
        plugins_dir=plugins_dir,
        output_dir=output_dir,
        num_examples=num_samples,
        batch_size=batch_size,
        run_as_daemon=as_daemon
    )
    publisher.publish_data()

if __name__ == "__main__":
    app()
