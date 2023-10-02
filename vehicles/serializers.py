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
            "active",
            "branch",
        )


class VehiclesResponseSerializer(serializers.ModelSerializer):
    branch = BranchesSimpleSerializer()
    last_movement = serializers.SerializerMethodField()

    class Meta:
        model = Vehicles
        fields = (
            "id",
            "type_vehicle",
            "vehicle_plate",
            "last_movement",
            "active",
            "branch",
        )

    def get_last_movement(self, obj):
        from fleets_availabilities.models import FleetsAvailabilities
        from fleets_availabilities.serializers import (
            FleetsAvailabilitiesVehiclesSerializer,
        )

        fleet = FleetsAvailabilities.objects.filter(vehicle=obj.id).last()

        if fleet:
            serializer = FleetsAvailabilitiesVehiclesSerializer(fleet)

            return serializer.data

        return None


class VehiclesSimpleSerializer(serializers.ModelSerializer):
    branch = BranchesSimpleSerializer()
    last_movement = serializers.SerializerMethodField()

    class Meta:
        model = Vehicles
        fields = (
            "id",
            "vehicle_plate",
            "last_movement",
            "active",
            "branch",
        )

    def get_last_movement(self, obj):
        from fleets_availabilities.models import FleetsAvailabilities
        from fleets_availabilities.serializers import (
            FleetsAvailabilitiesVehiclesSerializer,
        )

        fleet = FleetsAvailabilities.objects.filter(vehicle=obj.id).last()

        if fleet:
            serializer = FleetsAvailabilitiesVehiclesSerializer(fleet)

            return serializer.data

        return None
