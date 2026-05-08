from rest_framework import serializers
from .models import Profile
from apps.permissions.models import Permission

class ProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')

    allowed_routes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
        source='permissions'
    )
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        source='permissions',
        many=True,
        write_only=True
    )

    class Meta:
        model = Profile
        fields = ['id', 'user', 'user_name', 'allowed_routes', 'permission_ids']