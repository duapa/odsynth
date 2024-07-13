class ObjectModelValidationException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DataWritePreparationException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
