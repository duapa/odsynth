import secrets
from abc import ABC, abstractmethod
from typing import Any, List

DEFAULT_MAX_COUNT = 5


class DataElement(ABC):
    """An in memory representation of the schema of an item of data"""

    @property
    @abstractmethod
    def field_name(self) -> str:
        """Returns field name of a record or primitive fields"""
        raise NotImplementedError("'field_name' must be implemented in a subclass")

    @abstractmethod
    def generate_data(self):
        """Generates data based on schema or primitive data provider"""
        raise NotImplementedError("'generate_data' must be implemented in a subclasses")

    @property
    @abstractmethod
    def depth(self) -> int:
        """Returns the depth of the object tree"""
        raise NotImplementedError("Property '.depth' must be implemented in subclass")


class Record(DataElement):
    """Generates a record type of data element that contains other record types
    or primitive fields"""

    def __init__(self, field_name: str, max_count: int = 0, is_array=False):
        self._field_name = field_name
        self._children: List[DataElement] = []
        self._max_count = max_count
        self._is_array = is_array

    @property
    def field_name(self) -> str:
        """Returns the field name of the record"""
        return self._field_name

    @field_name.setter
    def field_name(self, value: str):
        self._field_name = value

    @property
    def children(self) -> List[DataElement]:
        return self._children

    @property
    def max_count(self):
        if self._max_count == 0:
            return secrets.randbelow(DEFAULT_MAX_COUNT + 1)
        return secrets.randbelow(self._max_count + 1)

    def add(self, element: DataElement):
        """Add a data element (Record or Field) to the list of fields of a
        record."""
        self._children.append(element)
        return self

    def __generate_data_array(self):
        """Generates an array of data items based on the schema of the record."""
        composite = []
        for _ in range(self.max_count):
            composite.append(self.__generate_data())
        return composite

    def __generate_data(self):
        """Generate a single data point based on the schema of the record"""
        child_data = {}
        for component in self._children:
            field_name = component.field_name
            data = component.generate_data()
            child_data.update({field_name: data})
        return child_data

    def generate_data(self):
        """Generate data based on the schema of the record"""
        if self._is_array:
            return self.__generate_data_array()
        return self.__generate_data()

    @property
    def depth(self):
        max_depth = 0
        for child in self._children:
            depth = child.depth
            if depth > max_depth:
                max_depth = depth
        return max_depth + 1


class Field(DataElement):
    """Generates a primitive data type (string, float, int, bool, etc)"""

    def __init__(self, kwargs):
        self._field_name = None
        self._kwargs = kwargs

    @property
    def field_name(self):
        return self._field_name

    @field_name.setter
    def field_name(self, value: str):
        self._field_name = value

    @property
    def provider_kwargs(self):
        return self._kwargs

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """Gets an identifying name for the provider.
        The provider name when specified in the schema is used to select the
        provider class that is used to generate the
        """
        raise NotImplementedError("Subclasses must implement get_name method")

    def generate_data(self) -> Any:
        raise NotImplementedError(
            "Data generation of a provider must be implemented in subclass"
        )

    @property
    def depth(self):
        return 1
