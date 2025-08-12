from django.db import models


class TestModel(models.Model):
    store_json = models.JSONField(null=True, blank=True)
