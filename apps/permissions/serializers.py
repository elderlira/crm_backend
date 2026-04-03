from rest_framework import serializers
from .models import Profile, Permission, ProfilePermission


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Permission

        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile

        fields = "__all__"


class ProfilePermissionSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProfilePermission

        fields = "__all__"