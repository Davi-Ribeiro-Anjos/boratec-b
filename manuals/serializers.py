from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer
from branches.serializers import BranchesSimpleSerializer

# from epis_items.serializers import EPIsItemsResponseSerializer

from .models import Manuals


class ManualsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuals
        fields = (
            "id",
            "title",
            "file",
            "system",
            "module",
            "author",
        )


class ManualsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuals
        fields = (
            "id",
            "title",
            "file",
            "system",
            "module",
        )
