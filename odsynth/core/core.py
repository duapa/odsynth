from abc import ABC, abstractmethod
from random import randint
from typing import List


class Component(ABC):
    @property
    def field_name(self) -> str:
        """Returns field name of component"""
        raise NotImplementedError("field_name must be implemented in subclass")

    def generate_data(self):
        """Returns a dictionary representation of the generated data"""
        raise NotImplementedError("to_dict must be implemented in subclasses")


class Composite(Component):
    def __init__(self, field_name: str):
        self._field_name = field_name
        self._children: List[Component] = []

    @property
    def field_name(self):
        return self._field_name

    @field_name.setter
    def field_name(self, value: str):
        self._field_name = value

    def add(self, component: Component):
        self._children.append(component)
        return self

    def generate_data(self):
        child_data = {}
        for component in self._children:
            field_name = component.field_name
            data = component.generate_data()
            child_data.update({field_name: data})
        return child_data


class Plural(Component):
    def __init__(self, field_name: str, max_count: int = 0):
        self._children: List[Component] = []
        self._field_name = field_name

        if max_count == 0:
            self._max_count = randint(1, 10)
        else:
            self._max_count = randint(1, max_count)

    @property
    def field_name(self):
        return self._field_name

    @field_name.setter
    def field_name(self, value: str):
        self._field_name = value

    def add(self, component: Component):
        self._children.append(component)
        return self

    def generate_data(self):
        composite = []

        for _ in range(self._max_count):
            child_data = {}
            for component in self._children:
                field_name = component.field_name
                data = component.generate_data()
                child_data.update({field_name: data})
            composite.append(child_data)

        return composite


class Provider(Component):
    def __init__(self, **kwargs):
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

    @provider_kwargs.setter
    def provider_kwargs(self, value: dict):
        self._kwargs = value

    def generate_data(self):
        raise NotImplementedError(
            "Data generation of a provider must be implemented in subclass"
        )
