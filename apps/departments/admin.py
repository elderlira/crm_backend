from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "client",
        "name",
        "message",
        "active"
    )

    list_filter = ("active", "client")

    search_fields = ("name",)