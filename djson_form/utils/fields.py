import copy

from django import forms
from abc import ABC, abstractmethod


class FieldFactory(ABC):
    @abstractmethod
    def create_field(self, **kwargs) -> forms.Field:
        pass


class StringFieldFactory(FieldFactory):
    def create_field(self, **kwargs) -> forms.Field:
        return forms.CharField(**kwargs)


class IntegerFieldFactory(FieldFactory):
    def create_field(self, **kwargs) -> forms.Field:
        return forms.IntegerField(**kwargs)


class BooleanFieldFactory(FieldFactory):
    def create_field(self, **kwargs) -> forms.Field:
        return forms.BooleanField(**kwargs)


class FieldGenerator:
    _factories = {
        "str": StringFieldFactory(),
        "int": IntegerFieldFactory(),
        "bool": BooleanFieldFactory(),
    }

    @classmethod
    def generate(cls, type_name: str, **kwargs) -> forms.Field:
        kwargs_ = copy.copy(kwargs)
        kwargs_.pop("type")
        factory = cls._factories.get(type_name)
        if not factory:
            raise ValueError(f"Unknown field type: {type_name}")
        return factory.create_field(**kwargs_)
