import typer

from ..schema import Schema

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
    formatter: str = typer.Option(
        None,
        help="Formatter used to render the generated data. Default = List of Dicts",
    ),
):
    schema = Schema(schema_file=schema_spec_file).build_generator(
        num_examples=num_samples, batch_size=batch_size, formatter=formatter
    )
    data = schema.get_data()
    print(data)


def main():
    app()
