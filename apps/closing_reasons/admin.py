from django.contrib import admin    
from .models import ClosingReason

@admin.register(ClosingReason)
class ClosingReasonAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "reason",
        "funnel",
        "department",
        "active"
    )

    list_filter = ("active", "department")

    search_fields = ("reason",)