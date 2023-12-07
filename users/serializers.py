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


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)
        extra_kwargs = {
            "email": {
                "write_only": True,
            },
        }
