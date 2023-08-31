from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer

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


class EPIsSizesRequestsSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = EPIsSizes
        fields = ("id", "size", "quantity", "item")
        depth = 1

    def get_item(self, obj):
        from epis_items.serializers import EPIsItemsRequestsSerializer

        serializer = EPIsItemsRequestsSerializer(obj.item)

        return serializer.data
