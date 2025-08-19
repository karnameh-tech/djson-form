from urllib.parse import urlencode

from djson_form.models import JSONSchema
from djson_form.forms import DynamicForm
from djson_form.utils.submit import SubmitProcessor

from django.shortcuts import render, redirect
from django.contrib import messages


def replace_query_params(request, schema: dict):
    request_body = request.POST.dict()
    query_params = request.GET.dict()
    request_body.pop("csrfmiddlewaretoken")
    for k, v in request_body.items():
        query_params[k] = v
    for k, v in schema.get("fields", {}).items():
        if not request_body.get(k):
            query_params.pop(k, None)
    return f"{request.path}?{urlencode(query_params)}"


def dynamic_form_view(request, object_slug):
    schema_obj: JSONSchema = JSONSchema.objects.get(slug=object_slug)

    if request.method == 'POST':
        form = DynamicForm(request.POST, schema=schema_obj.schema)
        if form.is_valid():
            SubmitProcessor().process(
                submit_type=schema_obj.schema.get("submit", {}).get("type"),
                json_schema=schema_obj.schema,
                form_data=request.POST.dict(),
                query_params=request.GET.dict(),
                form=form,
            )
            if form.is_valid():
                messages.success(request, schema_obj.schema.get("submit", {}).get("success_message", "Saved successfully."))
            else:
                context = {
                    'opts': JSONSchema._meta,
                    'form': form,
                    'original': schema_obj,
                    'title': f'{schema_obj.schema.get("title", schema_obj.name)}',
                    "query_params": request.GET.dict(),
                }
                return render(request, 'admin/json_schema_form.html', context)
        else:
            messages.error(request, schema_obj.schema.get("submit", {}).get("error_message", form.errors.as_text()))
        return redirect(replace_query_params(request, schema_obj.schema))
    else:
        params = {
            k: v
            for k, v in request.GET.dict().items()
            if v not in ["off", "false", False]
        }
        form = DynamicForm(schema=schema_obj.schema, initial=params)

    context = {
        'opts': JSONSchema._meta,
        'form': form,
        'original': schema_obj,
        'title': f'{schema_obj.schema.get("title", schema_obj.name)}',
        "query_params": request.GET.dict(),
    }

    return render(request, 'admin/json_schema_form.html', context)
