from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer
from epis_items.models import EPIsItems
from epis_items.serializers import EPIsItemsSimpleSerializer

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
    epis_items = serializers.SerializerMethodField()

    class Meta:
        model = EPIsGroups
        fields = (
            "id",
            "name",
            "epis_items",
        )
        depth = 1

    def get_epis_items(self, obj):
        epis_items = EPIsItems.objects.filter(group=obj)
        serializer = EPIsItemsSimpleSerializer(epis_items, many=True)
        return serializer.data
