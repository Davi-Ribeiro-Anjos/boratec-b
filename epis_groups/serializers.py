from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer

from .models import EPIsGroups


class EPIsGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPIsGroups
        fields = (
            "id",
            "name",
            "author",
        )


class EPIsGroupsResponseSerializer(serializers.ModelSerializer):
    author = EmployeesSimpleSerializer()

    class Meta:
        model = EPIsGroups
        fields = (
            "id",
            "name",
            "author",
        )
        depth = 1
