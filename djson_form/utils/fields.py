import copy

from django import forms
from django.utils.module_loading import import_string
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
    def __init__(self) -> None:
        self._factories = {
            "str": StringFieldFactory(),
            "int": IntegerFieldFactory(),
            "bool": BooleanFieldFactory(),
        }

    def generate(self, type_name: str, **kwargs) -> forms.Field:
        kwargs_ = copy.copy(kwargs)
        kwargs_.pop("type")
        factory = self._factories.get(type_name)
        if not factory:
            raise ValueError(f"Unknown field type: {type_name}")
        if kwargs_.get("validators"):
            kwargs_["validators"] = self.handle_validators(
                kwargs_["validators"]
            )
        return factory.create_field(**kwargs_)

    # TODO: clean code
    def handle_validators(self, validators_data: list) -> list:
        validators = []
        for validator in validators_data:
            if validator.get("type") == "callable":
                function_args = []
                if validator.get("args"):
                    for arg in validator.get("args", []):
                        if arg.get("type") == "int":
                            function_args.append(int(arg.get("value")))
                        if arg.get("type") == "str":
                            function_args.append(str(arg.get("value")))
                validators.append(
                    import_string(validator.get("callable"))(
                        *function_args
                    )
                )
            else:
                continue
        return validators
