# Data Synthesizer

This project demonstrates produces a python application that can be configured to generate "any" kind of fake data, given a schema. The solution relies on the [Composite Pattern](https://refactoring.guru/design-patterns/composite) to build an in-memory representation of the schema and consequently generate a python-dictionary example of the data specified by the schema.

This project may be used for generating data for exploratory cases at the beginning of ETL applications, benchmarking, fun projects etc.
The following providers, some based on `faker's` data generators have been implemented
* [random_int](./src/data_generator/primitives/providers/random_int.py)
* [first_name](./src/data_generator/primitives/providers/simple_text.py)
* [last_name](./src/data_generator/primitives/providers/simple_text.py)

The possibility of extending this solution will be added by implementing a plugins architecture which should contain 'user-added' data generators. Users can then specify these providers in their schemas

## Dependencies
* See [requirements.txt](./requirements.txt)

## Usage
Current iteration produces one data item for a fictitous scenario where an adult is responsible for a number of children

```sh
cd src

python main.py

```

The example schema from this example is shown below:

```python
data_schema = {
    "firstname": {"provider": "first_name"},
    "lastname": {"provider": "last_name"},
    "plural_children": {
        "fields": {
            "firstname": {"provider": "first_name"},
            "lastname": {"provider": "last_name"}
        },
        "max_count":20
    },
    "age": {
        "provider": "random_int",
        "provider_args": {
            "min": "25",
            "max": "55"
        }     
    }
}
generated_data = generate_data(schema=data_schema)
    
print(generated_data)

```

This produces an output like

```json
{'firstname': 'Bruce', 'lastname': 'Henderson', 'children': [{'firstname': 'George', 'lastname': 'Clayton'}, {'firstname': 'Brianna', 'lastname': 'Mosley'}, {'firstname': 'Jason', 'lastname': 'Armstrong'}, {'firstname': 'David', 'lastname': 'Mckee'}, {'firstname': 'Monica', 'lastname': 'Harper'}, {'firstname': 'Ann', 'lastname': 'Osborn'}, {'firstname': 'Ryan', 'lastname': 'Case'}, {'firstname': 'Joseph', 'lastname': 'Levine'}, {'firstname': 'Laura', 'lastname': 'Hernandez'}], 'age': 37}

```

# Extensibility
Adding user-defined `Providers` is possible by adding an extension python file to the [provider plugins folder](/src/data_generator/provider_plugins/). [An example for creating random integers is available here](/src/data_generator/provider_plugins/random_int.py)

# Next Steps
* Implement system for loading plugins from an absolute path
* Build CLI for generating data
* Build renderers for Spark Pandas etc
* Build Data -> S3 utility
* Build Data -> Kafka utility
* Any other ideas