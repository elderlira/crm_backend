from rest_framework import serializers
from .models import ClosingReason


class ClosingReasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClosingReason

        fields = [
            "id",
            "reason",
            "funnel",
            "department",
            "active",
            "message"
        ]