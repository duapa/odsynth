# Yaml Schema + Faker == ODSynth

This project produces a python application that can be configured to generate "any" kind of fake data, given a schema. The solution relies on the [Composite Pattern](https://refactoring.guru/design-patterns/composite) to build an in-memory representation of the schema and consequently generate a python-dictionary example of the data specified by the schema.

This project may be used for generating data for exploratory cases at the beginning of ETL applications, benchmarking, fun projects etc.
The following providers, some based on `faker's` data generators have been implemented
* [random_int](./odsynth/providers/random_int.py)
* [first_name](./odsynth/providers/simple_text.py)
* [last_name](./odsynth/providers/simple_text.py)


It is possible for developers to implement their own _data providers_ for their own custom cases. Users can then specify these providers in their schemas.

## Dependencies
* See [setup_config.toml](./setup_config.toml)

## Usage
Users can specify a plugins directory where additional Primitive data generators are stored. Run `main.py --help` for instructions.

### Example
`python odsynth/entry_points/demo.py --schema-spec=./sample_schema/schema_plural.yaml --plugins-dir=./sample_user_plugins --num-samples=3`

This example uses the schema at [./sample_schema/schema.yaml](./sample_schema/schema.yaml) which simulates the scenario of a parent having multiple children to produce an output similar what is shown below:

```json
{
    "firstname": "Bruce",
    "lastname": "Henderson",
    "children": [
        {"firstname": "George", "lastname": "Clayton"},
        {"firstname": "Brianna", "lastname": "Mosley"},
    ],
    "age": 37,
    "ssn": "604-35-3570"
}
```
**Note:** The specification of the schema and user plugin folders is not restricted to relative paths.

## Data Transformers
(Experimental) In the generation of the data, the user can specify a transformer which transforms the data which is inherently a list of dictionary objects to any other form specified by the user. Currently the following transformers are available:
* [JsonTransformer](./odsynth/transformers/json_transformer.py)
* [PandasDataframeTransformer](./odsynth/transformers/pandas_transformer.py)

# Extensibility
Extending the solution by adding user-defined providers is possible by creating your own plugins in a 'plugin folder' and specifying the plugin folder when calling the application. An example provider which uses `faker`'s `ssn` provider to generate fictitious American Social Security Numbers is available at [./sample_user_plugins](./sample_user_plugins/ssn.py)

# Development Roadmap
* [ ] Add a logger
* [ ] Improve DOM Validation
* [ ] Data Transformer for Spark
* [ ] Add support for optionals
* [x] Build Data Transformer for Pandas
* [x] Build Data Transformer for XML
* [x] Build Data Writer for XML
* [x] Build Data Transformer for JSON
* [x] Build Data Writer for JSON
* [ ] Build Data Writers for:
    * [ ] S3
    * [ ] Kafka
    * [ ] (Possibly) to REST APIs
    * [ ] (Possibly) for Metrics Systems like Prometheus
* [ ] Implement a plugin system for users to add their own code(Providers, Writers and Transformers) in their own local system
* [ ] (Possibly) Add examples for Dockerized deployment of Publishers
* [ ] Add Code and User documentation
* [ ] Add CICD Pipeline for deploying python package to PyPi
* [ ] Improve Local Python Packaging
