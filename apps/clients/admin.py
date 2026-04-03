from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "active",
        "created_at"
    )

    list_filter = ("active", )

    search_fields = ("name", )