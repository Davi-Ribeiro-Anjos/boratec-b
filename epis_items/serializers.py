from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer
from epis_sizes.models import EPIsSizes
from epis_sizes.serializers import EPIsSizesSimpleSerializer

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
    epis_sizes = serializers.SerializerMethodField()
    validity = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = EPIsItems
        fields = ("id", "description", "validity", "ca", "epis_sizes")
        depth = 1

    def get_epis_sizes(self, obj):
        epis_sizes = EPIsSizes.objects.filter(item=obj)
        serializer = EPIsSizesSimpleSerializer(epis_sizes, many=True)
        return serializer.data
