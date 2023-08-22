from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer
from branches.serializers import BranchesSimpleSerializer

from .models import Clients, ClientsBranches


class ClientsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = (
            "id",
            "name",
            "document",
        )


class ClientsBranchesSerializer(serializers.ModelSerializer):
    branch = BranchesSimpleSerializer()
    client = ClientsSimpleSerializer()

    class Meta:
        model = ClientsBranches
        fields = ("id", "branch", "client", "balance", "type_pallet")
        depth = 1


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = (
            "id",
            "name",
            "document",
            "observation",
            "type_registration",
            "author",
            "branches",
        )


class ClientsResponseSerializer(serializers.ModelSerializer):
    author = EmployeesSimpleSerializer()
    # branches = ClientsBranchesSerializer(many=True, read_only=True)

    class Meta:
        model = Clients
        fields = (
            "id",
            "name",
            "document",
            "observation",
            "type_registration",
            "author",
            "branches",
        )
        depth = 1
