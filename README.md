# ODSynth

ODSynth generates samples of synthetic data for you, based on the expected schema of your data. This project may be used for generating data for:
* Seeding your ETL applications
* Benchmarking of ETL applications
* Producing data in various formats (json, delimited text, xml, etc)

With the plugin system, developers can use their 'providers' locally in their own applications.

##  Core Idea
[See core idea for this project here](./docs/core_idea.md)

## How it works
1. Specify a schema. [See an example here](./sample_schema/flat_schema.yaml). The providers specify the type of data to be generated. (For example `first_name`, `last_name` etc.)
1. Use the schema to **generate data** in memory or **publish data** to a medium


## Installation
A proper python package for this application is not yet available, so users must clone the repo and install the Python package locally.

```sh
git clone https://github.com/kbaafi/data-synthesizer.git
cd data-synthesizer
# Optional
# python -m venv venv
pip install -e .
```
## Basic Usage
### Use 'synth' to generate json data
`synth --schema-spec-file=../schema.yaml --format=json --num-samples=3`
### Use 'synth' to generate csv data
`synth --schema-spec-file=../flat_schema.yaml --format=txt --num-samples=3 --formatter-arg delimiter=comma`

Delimiter may be one of 'comma', 'tab' or 'pipe'

### Use the API in your own code
```python
from odsynth.schema import Schema

def generate_data():
    num_samples=3
    batch_size=5                          # Batch size can be greater than num_samples
    format="txt"                          # Format can be json,xml,txt,pandas
    formatter_args=["delimiter=comma"]    # Depending on formatter, args may need to be provided. Default is None
    schema_spec_file="./sample_schema/flat_schema.yaml" # CSV formatter expects a tabular schema.
                                                        # XML, JSON, Pandas and Base Formatters can accept
                                                        # hierarchical data

    generator = Schema(schema_file=schema_spec_file).build_generator(
        num_examples=num_samples,
        batch_size=batch_size,
        format=format,
        formatter_args=formatter_args,
    )
    data = generator.get_data()

    # Prints generated data in csv format
    print(data)
```

### Use 'publish' to load synthetic data to local disc in XML format
Publish 100 samples of schema specified in `flat_schema.yaml`, 10 examples per batch.

`publish --schema-spec-file=../flat_schema.yaml --format=xml --writer=local_disc --writer-arg output_dir=../odsynth_out --num-samples=100 --batch-size=10`

> For more on the data generator and the data publisher, see the help pages for synth and publish
`publish --help` or `synth --help`

## Schemas and Providers
An example schema is shown below. This schema simulates the scenario of a parent responsible for up to 5 children. Providers are responsible for generating the primitive fields that comprise the record. [An example of a provider that generates a random integer can be found here](./odsynth/providers/random_int.py)
```yaml
fields:
  parent_firstname:
    provider: first_name
  parent_lastname:
    provider: last_name
  children:
    fields:
      firstname:
        provider: first_name
      lastname:
        provider: last_name
    max_count: 5
    is_array: true
  parent_age:
    provider: random_int
    provider_args:
      min: 25
      max: 55
  parent_ssn:
    provider: ssn
```
This schema is expected generated a data point that looks like this:

```json
{
    "parent_first_name": "Christopher", "parent_lastname": "Villegas",
    "children": [
        {"firstname": "Jason", "lastname": "Rogers"},
        {"firstname": "Andrea", "lastname": "Young"},
        {"firstname": "Michelle", "lastname": "Kaiser"}
    ],
    "parent_age": 43,
    "parent_ssn": "269-11-8507"
}
```

Currently ODSynth implements the following Providers from [Faker](https://github.com/joke2k/faker)
* [First Name](./odsynth/providers/simple_text.py)
* [Last Name](./odsynth/providers/simple_text.py)
* [Text](./odsynth/providers/simple_text.py)
* [Random Integer](./odsynth/providers/random_int.py)
* [Social Security Number](./odsynth/providers/ssn.py)

We hope to be able to develop more Providers in the future.
## Formatters
Generated data can be formatted into the following formats for use in memory or storage on disc:
* [Json](./odsynth/formatters/json_formatter.py)
* [XML](./odsynth/formatters/xml_formatter.py)
* [Delimited Text (csv, tsv, pipe delimited)](./odsynth/formatters/delimited_text_formatter.py)
* [Pandas](./odsynth/formatters/pandas_formatter.py)

## Writers
Writers work with the publishing system to write generated data to a specified medium. Currently the [local_disc](./odsynth/writers/disc_writer.py) writer has been implemented. Writers are primarily responsible for writing data to a destination medium which could take any form, e.g. S3, Azure Blob Storage, REST EndPoint, etc.

## Plugins and the ODSYNTH_HOME
It is possible for developers to plugin in their own providers, formatters and writers to the Data Synthesis system by loading the user added components from the **ODSYNTH_HOME** directory.  The ODSYNTH_HOME is  specified by setting the environment variable `ODSYNTH_HOME`

```sh
export ODSYNTH_HOME=./sample_home_folder
```

An ODSYNTH Home folder is expected to have the following subfolders the various developer plugins:
1. **providers** for user added providers
1. **formatters** for user added formatters
1. **writers** for user added writers


The plugins system will load all providers, formatters and writers from the HOME folder.

# Development Roadmap
* [x] Build Data Formatter for Pandas
* [x] Build Data Formatter for XML
* [x] Build Data Writer for XML
* [x] Build Data Formatter for JSON
* [x] Build Data Writer for JSON
* [x] Build Formatter for Delimited Text
* [ ] Add a logger (Under consideration)
* [ ] Add some form of support for Py Faker's Locales
* [x] Improve DOM Validation (Ongoing)
* [ ] Data Transformer for Spark
* [ ] Add support for optional fields
* [ ] Build Data Writers for:
    * [ ] S3
    * [ ] Kafka
    * [ ] (Possibly) to REST APIs
* [ ] Implement a plugin system for users to add their own code(Providers, Writers and Transformers) in their own local system
* [ ] (Possibly) Add examples for Dockerized deployment of Publishers
* [ ] Add Code and User documentation
* [ ] Add CICD Pipeline for deploying python package to PyPi
* [ ] Improve Local Python Packaging
