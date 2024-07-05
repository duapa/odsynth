import typer
from typing_extensions import Annotated

from odsynth.generator import DataGenerator
from odsynth.transformers import TransformerFactory
from odsynth.utils import load_yaml

app = typer.Typer()


@app.command()
def main(
    schema_spec_file: str = typer.Option(
        help="Location of schema definition for data generation"
    ),
    num_samples: int = typer.Option(10, help="Number of samples to be generated"),
    batch_size: int = typer.Option(
        5, help="Size of batch when generating data in batches"
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
        transformer=TransformerFactory.get_transformer(transformer),
        batch_size=batch_size,
    )

    data = generator.get_data()
    print(data)


if __name__ == "__main__":
    app()
