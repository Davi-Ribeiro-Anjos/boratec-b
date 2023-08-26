from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer

# from epis_items.serializers import EPIsItemsResponseSerializer

from .models import EPIsSizes


class EPIsSizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPIsSizes
        fields = (
            "id",
            "size",
            "quantity",
            "quantity_minimum",
            "quantity_provisory",
            "item",
            "author",
        )


class EPIsSizesResponseSerializer(serializers.ModelSerializer):
    author = EmployeesSimpleSerializer()
    # item = EPIsItemsResponseSerializer()

    class Meta:
        model = EPIsSizes
        fields = (
            "id",
            "size",
            "quantity",
            "quantity_minimum",
            "quantity_provisory",
            # "item",
            "author",
        )
        depth = 1


class EPIsSizesSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPIsSizes
        fields = (
            "id",
            "size",
            "quantity",
            "quantity_minimum",
            "quantity_provisory",
        )
