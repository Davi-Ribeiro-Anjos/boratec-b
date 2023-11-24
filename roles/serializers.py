from rest_framework import serializers

from .models import Roles


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = (
            "id",
            "name",
            "active",
        )


class RolesResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = (
            "id",
            "name",
        )


class RolesSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = (
            "id",
            "name",
        )
