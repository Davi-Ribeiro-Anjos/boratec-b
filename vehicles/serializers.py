from rest_framework import serializers

from branches.serializers import BranchesSimpleSerializer

from .models import Vehicles


class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = (
            "id",
            "type_vehicle",
            "vehicle_plate",
            "vehicle_mileage",
            "renavam",
            "model_vehicle",
            "observation",
            "last_movement",
            "active",
            "branch",
        )


class VehiclesResponseSerializer(serializers.ModelSerializer):
    branch = BranchesSimpleSerializer()

    class Meta:
        model = Vehicles
        fields = (
            "id",
            "type_vehicle",
            "vehicle_plate",
            "vehicle_mileage",
            "renavam",
            "model_vehicle",
            "observation",
            "last_movement",
            "active",
            "branch",
        )


class VehiclesSimpleSerializer(serializers.ModelSerializer):
    branch = BranchesSimpleSerializer()

    class Meta:
        model = Vehicles
        fields = (
            "id",
            "vehicle_plate",
            "last_movement",
            "active",
            "branch",
        )
