from data_generator.synth import generate_data

def main():
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

if __name__ == "__main__":
    main()