from rest_framework import serializers

from django.contrib.auth.models import User


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_superuser",
            "is_active",
        )


class UsuariosSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_active",
        )


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
        extra_kwargs = {
            "username": {
                "write_only": True,
            },
            "password": {
                "write_only": True,
            },
        }
