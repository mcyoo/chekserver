from django.contrib import admin
from . import models


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "change")

