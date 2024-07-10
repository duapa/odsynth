import typer

from ..generator import DataGenerator

app = typer.Typer()


@app.command()
def generate_data_command(
    schema_spec_file: str = typer.Option(
        help="Location of schema definition for data generation"
    ),
    num_samples: int = typer.Option(1, help="Number of samples to be generated"),
    batch_size: int = typer.Option(
        1, help="Size of batch when generating data in batches"
    ),
    plugins_dir: str = typer.Option(
        None, help="Location for user added data generation providers."
    ),
    transformer: str = typer.Option(
        None,
        help="Transformer used to render the generated data. Default = List of Dicts",
    ),
):
    generator = DataGenerator(
        schema_spec_file=schema_spec_file,
        plugins_dir=plugins_dir,
        num_examples=num_samples,
        transformer_name=transformer,
        batch_size=batch_size,
    )

    data = generator.get_data()
    print(data)


def main():
    app()
