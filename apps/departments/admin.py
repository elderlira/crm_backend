from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "company",
        "name",
        "message",
        "active"
    )

    list_filter = ("active", "company")

    search_fields = ("name",)