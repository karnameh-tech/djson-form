from django.contrib import admin
from djson_form.models import JSONSchema
from djson_form.forms import JSONSchemaForm
from djson_form.views import dynamic_form_view
from django.urls import path


class JSONSchemaAdmin(admin.ModelAdmin):
    form = JSONSchemaForm
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_slug>/view/',
                self.admin_site.admin_view(dynamic_form_view),
                name='json_schema_test',
            ),
        ]
        return custom_urls + urls


admin.site.register(JSONSchema, JSONSchemaAdmin)
