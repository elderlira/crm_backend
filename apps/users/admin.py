from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserDepartment, UserCompanyDepartment

@admin.register(UserDepartment)
class UserDepartmentAdmin(admin.ModelAdmin):
    list_display = ("user", "department")

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "name", "company", "role", "away_message", "no_auto_assign", "see_department_tickets","is_online", "last_login", "last_logout")
    readonly_fields = ("last_login", "last_logout")

    fieldsets = UserAdmin.fieldsets + (
        ("CRM Info", {"fields": ("name", "phone", "company", "role", "away_message", "no_auto_assign", "see_department_tickets","is_online")}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("CRM Info", {"fields": ("email", "name", "company", "role","away_message", "no_auto_assign", "see_department_tickets")}),
    )

    search_fields = ("email", "name")
    ordering = ("email",)

@admin.register(UserCompanyDepartment)
class UserCompanyDepartment(admin.ModelAdmin):
    list_display = ("id","user","company","department","created_at")
    list_filter = ("company","department")
    search_fields = ("user__name","user__email","company__name","department__name")
    