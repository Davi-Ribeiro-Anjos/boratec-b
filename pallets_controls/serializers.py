from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer

from .models import PalletsControls


class PalletsControlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletsControls
        fields = [
            "id",
            "current_location",
            "type_pallet",
            "current_movement",
            "author",
        ]


class PalletsControlsResponseSerializer(serializers.ModelSerializer):
    author = EmployeesSimpleSerializer()

    class Meta:
        model = PalletsControls
        fields = [
            "id",
            "current_location",
            "type_pallet",
            "current_movement",
            "author",
        ]
        delth = 1
