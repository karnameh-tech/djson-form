import copy

from djson_form.models import JSONSchema
from djson_form.forms import DynamicForm

from django.shortcuts import render, redirect
from django.apps import apps


def store_form_in_model_field(
    app_label: str,
    model_name: str,
    field_name: str,
    object_id: int,
    value: dict,
):
    model = apps.get_model(app_label=app_label, model_name=model_name)
    obj = model.objects.get(id=object_id)
    value = copy.copy(value)
    value.pop("csrfmiddlewaretoken")
    setattr(obj, field_name, value)
    obj.save()


def dynamic_form_view(request, object_slug):
    schema_obj: JSONSchema = JSONSchema.objects.get(slug=object_slug)

    if request.method == 'POST':
        form = DynamicForm(request.POST, schema=schema_obj.schema)
        if form.is_valid():
            store_form_in_model_field(
                app_label=schema_obj.schema.get("submit", {}).get("app_label"),
                model_name=schema_obj.schema.get("submit", {}).get("model_name"),
                field_name=schema_obj.schema.get("submit", {}).get("field_name"),
                object_id=request.GET.get("object_id"),
                value=request.POST,
            )
            return redirect('.')
    else:
        form = DynamicForm(schema=schema_obj.schema)

    context = {
        'opts': JSONSchema._meta,
        'form': form,
        'original': schema_obj,
        'title': f'{schema_obj.schema.get("title", schema_obj.name)}',
    }

    return render(request, 'admin/json_schema_form.html', context)
