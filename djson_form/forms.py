import json

from django import forms
from djson_form.models import JSONSchema

from djson_form.utils.fields import field_generator


class PrettyJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=2, sort_keys=True, **kwargs)


class JSONSchemaForm(forms.ModelForm):
    class Meta:
        model = JSONSchema
        fields = '__all__'


class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        schema = kwargs.pop('schema', None)
        super().__init__(*args, **kwargs)

        if schema:
            fields = schema.get("fields")
            for field_name, field_def in fields.items():
                field_type: str = field_def.get("type")
                required: bool = field_def.get("required", False)
                label: str = field_def.get("label", field_name.title())
                help_text: str = field_def.get("help_text", "")

                self.fields[field_name] = field_generator(
                    type=field_type,
                    required=required,
                    label=label,
                    help_text=help_text,
                )
