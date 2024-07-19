ODSynth generates samples of synthetic data, based on the expected schema of your data. This project may be used for generating data for:

- Seeding your ETL applications
- Benchmarking of ETL applications
- Producing data in various formats (json, delimited text, xml, etc) on disc

With the plugin system, developers can use their own providers, formatters and writers locally in their own applications.

`Read the full documentation here <https://odsynth.readthedocs.io/>`_ 


Installation
-------------
``pip install odsynth``

Basic Usage
------------

Once installed you can use ``synth`` to generate synthetic data in the console or ``publish`` to generate data to a medium such as on local disc.

Using synth to generate json data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``synth --schema-spec-file=../schema.yaml --format=json --num-samples=3``

Using synth to generate csv data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``synth --schema-spec-file=../flat_schema.yaml --format=txt --num-samples=3 --formatter-arg delimiter=comma``

The delimiter may be one of 'comma', 'tab' or 'pipe'

Using ODSynth in your own code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

::

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

Use 'publish' to load synthetic data to local disc in XML format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Publish 100 samples of schema specified in ``flat_schema.yaml``, 10 examples per batch.

``publish --schema-spec-file=./sample_schema/flat_schema.yaml --format=xml --writer=local_disc --writer-arg output_dir=../odsynth_out --num-samples=100 --batch-size=10``

For more on the data generator and the data publisher, see the help pages for synth and publish
``publish --help`` or ``synth --help``

For the following schema: ::

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



The following output is expected: ::

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

License
-------

ODSynth is released under the MIT License. See `LICENSE`_ for details.

Credits
-------

-  `Faker`_


.. _Faker: https://github.com/joke2k/faker
.. _LICENSE: https://github.com/duapa/odsynth/blob/main/LICENSE
.. _documentation: https://odsynth.readthedocs.io/