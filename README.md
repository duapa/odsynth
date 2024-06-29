# Data Synthesizer

This project demonstrates produces a python application that can be configured to generate "any" kind of fake data, given a schema. The solution relies on the [Composite Pattern](https://refactoring.guru/design-patterns/composite) to build an in-memory representation of the schema and consequently generate a python-dictionary example of the data specified by the schema.

This project may be used for generating data for exploratory cases at the beginning of ETL applications, benchmarking, fun projects etc.
The following providers, some based on `faker's` data generators have been implemented
* [random_int](./src/data_generator/provider_plugins/random_int.py)
* [first_name](./src/data_generator/primitives/providers/simple_text.py)
* [last_name](./src/data_generator/primitives/providers/simple_text.py)

It is possible for developers to implement their own _data providers_ for their own custom cases. Users can then specify these providers in their schemas.

## Dependencies
* See [requirements.txt](./requirements.txt)

## Usage
Users can specify a plugins directory where additional Primitive data generators are stored. Run `main.py --help` for instructions.

### Example
`python src/main.py --schema-spec=./sample_schema/schema.yaml --plugins-dir=./sample_user_plugins/`

This example relies on the schema at [./sample_schema/schema.yaml](./sample_schema/schema.yaml) which simulates the scenario of a parent having multiple children and produces an output similar what is shown below:

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

# Extensibility
Extending the solution by adding user-defined providers is possible by creating your own plugins in a 'plugin folder' and specifying the plugin folder when calling the application. An example provider which uses `faker`'s `ssn` provider to generate fictitious American Social Security Numbers is available at [./sample_user_plugins](./sample_user_plugins/ssn.py)

# Next Steps
* Extend CLI for generating data
* Generalize user API for generating data
* Build renderers for Spark Pandas etc
* Build Data Publishers
    * Build Data -> S3 utility
    * Build Data -> Kafka utility
* Any other ideas