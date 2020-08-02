from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("token", "user_os", "user_ver")
    # count_photos.short_description = "photo count"
