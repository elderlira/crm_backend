from rest_framework import serializers
from .models import Label

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'etiqueta', 'cor', 'online', 'company']
        read_only_fields = ['id', 'company']