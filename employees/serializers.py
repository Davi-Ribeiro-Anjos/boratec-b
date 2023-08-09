from rest_framework import serializers

from branches.serializers import BranchesSimpleSerializer
from pj_complements.serializers import PJComplementsResponseSerializer
from users.serializers import UserSimpleSerializer

from .models import Employees


class CPFFormattedField(serializers.CharField):
    def to_representation(self, value):
        if len(value) == 11:
            return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"
        return value


class CNPJFormattedField(serializers.CharField):
    def to_representation(self, value):
        if len(value) == 14:
            return f"{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}"
        return value


class RGFormattedField(serializers.CharField):
    def to_representation(self, value):
        if len(value) == 9:
            return f"{value[:2]}.{value[2:5]}.{value[5:8]}-{value[8:]}"
        return value


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = (
            "id",
            "name",
            "gender",
            "date_birth",
            "rg",
            "cpf",
            "cnpj",
            "company",
            "type_contract",
            "role",
            "street",
            "number",
            "complement",
            "cep",
            "district",
            "city",
            "uf",
            "bank",
            "agency",
            "account",
            "pix",
            "date_admission",
            "status",
            "branch",
            "pj_complements",
            "user",
        )


class EmployeesResponseSerializer(serializers.ModelSerializer):
    branch = BranchesSimpleSerializer()
    pj_complements = PJComplementsResponseSerializer()
    user = UserSimpleSerializer()
    cpf = CPFFormattedField()
    cnpj = CNPJFormattedField()

    class Meta:
        model = Employees
        fields = (
            "id",
            "name",
            "cpf",
            "cnpj",
            "type_contract",
            "role",
            "bank",
            "agency",
            "account",
            "pix",
            "date_admission",
            "status",
            "branch",
            "pj_complements",
            "user",
        )
        depth = 1


class EmployeesSimpleSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Employees
        fields = (
            "id",
            "name",
            "user",
        )
        depth = 1
