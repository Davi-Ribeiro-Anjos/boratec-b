from rest_framework import serializers

from branches.serializers import BranchesSimpleSerializer
from pj_complements.serializers import PJComplementsResponseSerializer
from users.serializers import UserSimpleSerializer, UserLoginSerializer

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
            "email",
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
    user = UserSimpleSerializer()
    date_birth = serializers.DateField(format="%d/%m/%Y")
    rg = RGFormattedField()
    cpf = CPFFormattedField()
    cnpj = CNPJFormattedField()
    date_admission = serializers.DateField(format="%d/%m/%Y")
    branch = BranchesSimpleSerializer()
    pj_complements = PJComplementsResponseSerializer()

    class Meta:
        model = Employees
        fields = (
            "id",
            "name",
            "email",
            "date_birth",
            "rg",
            "cpf",
            "cnpj",
            "rg",
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
            "operation",
            "pix",
            "date_admission",
            "status",
            "branch",
            "pj_complements",
            "user",
        )
        depth = 1


class EmployeesResponsePJSerializer(serializers.ModelSerializer):
    branch = BranchesSimpleSerializer()
    pj_complements = PJComplementsResponseSerializer()
    user = UserSimpleSerializer()
    cnpj = CNPJFormattedField()
    rg = RGFormattedField()
    date_admission = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Employees
        fields = (
            "id",
            "name",
            "email",
            "cnpj",
            "type_contract",
            "role",
            "company",
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


class EmployeesPaymentsResponseSerializer(serializers.ModelSerializer):
    pj_complements = PJComplementsResponseSerializer()

    class Meta:
        model = Employees
        fields = (
            "id",
            "name",
            "email",
            "type_contract",
            "pj_complements",
        )
        depth = 1


class EmployeesSimpleSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Employees
        fields = (
            "id",
            "name",
            "email",
            "user",
        )
        depth = 1


class EmployeesLoginSerializer(serializers.ModelSerializer):
    user = UserLoginSerializer()
    branch = BranchesSimpleSerializer()

    class Meta:
        model = Employees
        fields = (
            "id",
            "name",
            "email",
            "branch",
            "user",
        )
        depth = 1
