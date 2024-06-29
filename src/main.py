import typer
from typing_extensions import Annotated

from data_generator.synth import generate_data

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
    generated_data = generate_data(schema_spec_file=schema_spec, plugins_dir=plugins_dir)
    print(generated_data)


if __name__ == "__main__":
    app()
