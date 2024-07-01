import typer
from typing_extensions import Annotated

from odsynth.data_generator import DataGenerator
from odsynth.transformers import JsonTransformer, PandasDataframeTransformer
from odsynth.utils import load_yaml

app = typer.Typer()


@app.command()
def main(
    schema_spec_file: str = typer.Option(
        help="Location of schema definition for data generation"
    ),
    num_samples: int = typer.Option(help="Number of samples to be generated"),
    plugins_dir: str = typer.Option(
        None, help="Location for user added data generation providers."
    ),
):
    generator = DataGenerator(
        schema_spec_file=schema_spec_file,
        plugins_dir=plugins_dir,
        num_examples=num_samples,
        transformer=PandasDataframeTransformer(),
    )
    for data in generator.yield_data():
        print(data, "\n")


if __name__ == "__main__":
    app()
