from django.contrib import admin
from .models import Department, CompanyDepartment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active")
    list_filter = ("active",)

@admin.register(CompanyDepartment)
class CompanyDepartmentAdmin(admin.ModelAdmin):
    list_display = ("company", "department")