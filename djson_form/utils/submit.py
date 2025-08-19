import copy

from django.apps import apps
from django.utils.module_loading import import_string
from django.forms import forms

from djson_form.utils.cast import Cast


class SubmitProcessor:
    def __init__(self) -> None:
        self._processors = {
            "save_form_in_model": self._save_form_in_model,
        }

    def process(self, submit_type: str, json_schema: dict, form_data: dict, query_params: dict, form):
        form_data_ = self._pop_form_data(form_data)
        processor = self._processors.get(submit_type)
        if not processor:
            raise ValueError(f"Unknown submit type: {submit_type}")
        processor(
            form_data=form_data_,
            json_schema=json_schema,
            query_params=query_params,
            form=form,
        )

    def _pop_form_data(self, form_data: dict):
        _form_data = copy.copy(form_data)
        _form_data.pop("csrfmiddlewaretoken")
        return _form_data

    def _save_form_in_model(self, form_data: dict, json_schema: dict, query_params: dict, form):
        save_in: str | None = json_schema.get("submit", {}).get("save_in", None)
        if not save_in:
            raise ValueError("save_in is required")

        if not query_params.get("object_id"):
            raise ValueError("object_id param is required")

        splitted_save_in: list = save_in.split(".")
        if len(splitted_save_in) != 3:
            raise Exception("Wrong save_in format")

        app_label, model_name, field_name = splitted_save_in
        model = apps.get_model(app_label=app_label, model_name=model_name)
        obj = model.objects.get(id=query_params.get("object_id"))
        if json_schema.get("validators"):
            self._handle_validators(
                json_schema.get("validators", []),
                obj,
                form,
            )
        setattr(obj, field_name, Cast(form_data, json_schema.get("fields", {})).to_python())
        obj.save()

    def _handle_validators(self, validators: list, obj, form: forms.Form):
        for validator in validators:
            if validator.get("type") == "callable":
                import_string(validator.get("callable"))(
                    obj,
                    form,
                )
