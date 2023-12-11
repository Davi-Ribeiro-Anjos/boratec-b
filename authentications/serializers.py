from rest_framework import serializers

from django.contrib.auth.models import User


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
