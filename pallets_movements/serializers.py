from rest_framework import serializers

from branches.serializers import BranchesSimpleSerializer
from employees.serializers import EmployeesSimpleSerializer

from .models import PalletsMovements


class PalletsMovementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletsMovements
        fields = (
            "id",
            "request",
            "date_request",
            "date_received",
            "vehicle_plate",
            "driver",
            "checker",
            "received",
            "quantity_pallets",
            "origin",
            "destiny",
            "author",
        )


class PalletsMovementsSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalletsMovements
        fields = (
            "id",
            "request",
            "date_request",
            "date_received",
            "vehicle_plate",
            "driver",
            "checker",
            "received",
            "quantity_pallets",
            "origin",
            "destiny",
            "author",
        )


class PalletsMovementsResponseSerializer(serializers.ModelSerializer):
    origin = BranchesSimpleSerializer()
    destiny = BranchesSimpleSerializer()
    author = EmployeesSimpleSerializer()
    date_request = serializers.DateTimeField(format="%d-%m-%Y")
    date_received = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = PalletsMovements
        fields = (
            "id",
            "request",
            "date_request",
            "date_received",
            "vehicle_plate",
            "driver",
            "checker",
            "quantity_pallets",
            "received",
            "origin",
            "destiny",
            "author",
        )
        depth = 1
