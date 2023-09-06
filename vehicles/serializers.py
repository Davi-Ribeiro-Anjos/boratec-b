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
            "vehicle_mileage",
            "renavam",
            "model_vehicle",
            "observation",
            "last_movement",
            "active",
            "branch",
        )

    def get_last_movement(self, obj):
        from fleets_availabilities.serializers import (
            FleetsAvailabilitiesSimplesSerializer,
        )

        fleet = obj.fleets_availabilities.all().order_by("-date_occurrence").first()

        if fleet:
            serializer = FleetsAvailabilitiesSimplesSerializer(fleet)

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
        from fleets_availabilities.serializers import (
            FleetsAvailabilitiesSimplesSerializer,
        )

        fleet = obj.fleets_availabilities.all().order_by("-date_occurrence").first()

        if fleet:
            serializer = FleetsAvailabilitiesSimplesSerializer(fleet)

            return serializer.data

        return None
