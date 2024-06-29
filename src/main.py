import typer
from typing_extensions import Annotated

from data_generator.synth import generate_data
from utils import load_yaml

app = typer.Typer()


@app.command()
def main(
    schema_spec: Annotated[
        str, typer.Option(help="Location of schema definition for data generation")
    ],
    plugins_dir: Annotated[
        str, typer.Option(help="Location for user added data generation providers.")
    ] = None,
):
    data_schema = load_yaml(schema_spec)
    generated_data = generate_data(schema=data_schema, plugins_dir=plugins_dir)
    print(generated_data)


if __name__ == "__main__":
    app()
