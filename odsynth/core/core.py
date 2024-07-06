from abc import ABC, abstractmethod
from random import randint
from typing import List

DEFAULT_MAX_COUNT = 5


class Component(ABC):
    @property
    def field_name(self) -> str:
        """Returns field name of component"""
        raise NotImplementedError("field_name must be implemented in subclass")

    def generate_data(self):
        """Returns a dictionary representation of the generated data"""
        raise NotImplementedError("generate_data must be implemented in subclasses")


class Composite(Component):
    def __init__(self, field_name: str, max_count: int = 0, is_array=False):
        self._field_name = field_name
        self._children: List[Component] = []
        self._max_count = max_count
        self._is_array = is_array

    @property
    def field_name(self):
        return self._field_name

    @property
    def max_count(self):
        if self._max_count == 0:
            return randint(1, DEFAULT_MAX_COUNT)
        return randint(1, self._max_count)

    @field_name.setter
    def field_name(self, value: str):
        self._field_name = value

    def add(self, component: Component):
        self._children.append(component)
        return self

    def __generate_data_array_format(self):
        composite = []
        for _ in range(self.max_count):
            composite.append(self.__generate_data())
        return composite

    def __generate_data(self):
        child_data = {}
        for component in self._children:
            field_name = component.field_name
            data = component.generate_data()
            child_data.update({field_name: data})
        return child_data

    def generate_data(self):
        if self._is_array:
            return self.__generate_data_array_format()
        return self.__generate_data()


class Provider(Component):
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

    def generate_data(self):
        raise NotImplementedError(
            "Data generation of a provider must be implemented in subclass"
        )
