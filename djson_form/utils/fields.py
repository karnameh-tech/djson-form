from django import forms


FIELDS_MAPPER = {
    "str": forms.CharField,
    "int": forms.IntegerField,
    "bool": forms.BooleanField,
    "date": forms.DateField,
    "float": forms.FloatField,
    "time": forms.TimeField,
    "datetime": forms.DateTimeField,
    "email": forms.EmailField,
    "file": forms.FileField,
    "url": forms.URLField,
}


def field_generator(
        type: str,
        required: bool,
        label: str,
        help_text: str,
):
    return FIELDS_MAPPER[type](
        required=required,
        label=label,
        help_text=help_text,
    )
