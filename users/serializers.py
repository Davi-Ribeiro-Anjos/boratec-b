from rest_framework import serializers

from django.contrib.auth.models import User, Group


class UserSerializer(serializers.ModelSerializer):
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


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class UserLoginSerializer(serializers.ModelSerializer):
    groups = GroupsSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "groups",
            "email",
            "is_staff",
            "is_superuser",
            "is_active",
        )
        depth = 1


class UserSimpleSerializer(serializers.ModelSerializer):
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
