from rest_framework import serializers

from vehicles.serializers import VehiclesSimpleSerializer
from employees.serializers import EmployeesSimpleSerializer

from .models import FleetsAvailabilities


class FleetsAvailabilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FleetsAvailabilities
        fields = (
            "id",
            "date_occurrence",
            "date_forecast",
            "date_release",
            "status",
            "service_order",
            "observation",
            "author",
            "vehicle",
        )


class FleetsAvailabilitiesResponseSerializer(serializers.ModelSerializer):
    author = EmployeesSimpleSerializer()
    vehicle = VehiclesSimpleSerializer()

    class Meta:
        model = FleetsAvailabilities
        fields = (
            "id",
            "date_occurrence",
            "date_forecast",
            "date_release",
            "status",
            "service_order",
            "observation",
            "author",
            "vehicle",
        )


class FleetsAvailabilitiesSimplesSerializer(serializers.ModelSerializer):
    author = EmployeesSimpleSerializer()

    class Meta:
        model = FleetsAvailabilities
        fields = (
            "id",
            "date_occurrence",
            "date_forecast",
            "date_release",
            "status",
            "service_order",
            "observation",
            "author",
        )
