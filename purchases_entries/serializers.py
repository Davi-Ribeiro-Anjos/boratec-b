from rest_framework import serializers

from purchases_requests.serializers import PurchasesRequestsSimpleSerializer
from employees.serializers import EmployeesSimpleSerializer

from .models import PurchasesEntries


class PurchasesEntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasesEntries
        fields = (
            "id",
            "observation",
            "file_1",
            "file_2",
            "file_3",
            "date_creation",
            "request",
            "author",
        )


class PurchasesEntriesResponseSerializer(serializers.ModelSerializer):
    author = EmployeesSimpleSerializer()
    request = PurchasesRequestsSimpleSerializer()

    class Meta:
        model = PurchasesEntries
        fields = (
            "id",
            "observation",
            "file_1",
            "file_2",
            "file_3",
            "date_creation",
            "request",
            "author",
        )
        depth = 1
