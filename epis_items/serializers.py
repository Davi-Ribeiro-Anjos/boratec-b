from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer

from .models import EPIsItems


class EPIsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPIsItems
        fields = ("id", "description", "validity", "ca", "group", "author")


class EPIsItemsResponseSerializer(serializers.ModelSerializer):
    author = EmployeesSimpleSerializer()

    class Meta:
        model = EPIsItems
        fields = ("id", "description", "validity", "ca", "author")
        depth = 1


class EPIsItemsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPIsItems
        fields = ("id", "description", "validity", "ca", "epis_sizes")
        depth = 1
