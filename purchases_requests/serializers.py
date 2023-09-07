from rest_framework import serializers

from branches.serializers import BranchesSimpleSerializer
from employees.serializers import EmployeesSimpleSerializer

from .models import PurchasesRequests


class PurchasesRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasesRequests
        fields = (
            "id",
            "number_request",
            "date_request",
            "date_expiration",
            "date_completion",
            "status",
            "department",
            "category",
            "payment_method",
            "paid",
            "observation",
            "attachment",
            "branch",
            "requester",
            "responsible",
            "author",
            "latest_updater",
        )


class PurchasesRequestsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasesRequests
        fields = (
            "id",
            "number_request",
            "date_request",
            "date_expiration",
            "date_completion",
            "status",
            "observation",
        )


class PurchasesRequestsResponseSerializer(serializers.ModelSerializer):
    branch = BranchesSimpleSerializer()
    requester = EmployeesSimpleSerializer()
    responsible = EmployeesSimpleSerializer()
    author = EmployeesSimpleSerializer()
    latest_updater = EmployeesSimpleSerializer()
    date_request = serializers.DateTimeField(format="%d/%m/%Y")
    date_expiration = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = PurchasesRequests
        fields = (
            "id",
            "number_request",
            "date_request",
            "date_expiration",
            "date_completion",
            "status",
            "department",
            "category",
            "payment_method",
            "paid",
            "observation",
            "attachment",
            "branch",
            "requester",
            "responsible",
            "author",
            "latest_updater",
        )
        depth = 1


class PurchasesRequestsEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasesRequests
        fields = (
            "number_request",
            "date_expiration",
            "date_completion",
            "status",
            "department",
            "category",
            "payment_method",
            "paid",
            "observation",
            "attachment",
            "responsible",
            "latest_updater",
        )
