from django.contrib import admin
from .models import Profile, Permission, ProfilePermission

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name"
    )

    search_fields = ("name", )

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = ("name", )

@admin.register(ProfilePermission)
class ProfilePermissionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "profile",
        "permission"
    )