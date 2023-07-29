from django.contrib.auth.models import User
from django.db.models import F

from rest_framework import serializers

from filiais.serializers import FiliaisSimplesSerializer
from pj_complementos.serializers import PJComplementosResponseSerializer
from usuarios.serializers import UsuariosSimplesSerializer

from .models import Funcionarios


class CPFFormattedField(serializers.CharField):
    def to_representation(self, value):
        # Verifica se o valor é um CPF válido
        if len(value) == 11:
            return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"
        return value


class CNPJFormattedField(serializers.CharField):
    def to_representation(self, value):
        # Verifica se o valor é um CNPJ válido
        if len(value) == 14:
            return f"{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}"
        return value


class RGFormattedField(serializers.CharField):
    def to_representation(self, value):
        # Verifica se o valor é um RG válido
        if len(value) == 9:
            return f"{value[:2]}.{value[2:5]}.{value[5:8]}-{value[8:]}"
        return value


class UsuariosSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_active",
        )


class FuncionariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionarios
        fields = (
            "id",
            "nome",
            "genero",
            "data_nascimento",
            "rg",
            "cpf",
            "cnpj",
            "empresa",
            "tipo_contrato",
            "cargo",
            "rua",
            "numero",
            "complemento",
            "cep",
            "bairro",
            "cidade",
            "uf",
            "banco",
            "agencia",
            "conta",
            "pix",
            "data_admissao",
            "ativo",
            "filial",
            "pj_complementos",
            "user",
        )


class FuncionariosResponseSerializer(serializers.ModelSerializer):
    filial = FiliaisSimplesSerializer()
    pj_complementos = PJComplementosResponseSerializer()
    user = UsuariosSimplesSerializer()
    cpf = CPFFormattedField()
    cnpj = CNPJFormattedField()

    class Meta:
        model = Funcionarios
        fields = (
            "id",
            "nome",
            "cpf",
            "cnpj",
            "tipo_contrato",
            "cargo",
            "banco",
            "agencia",
            "conta",
            "pix",
            "data_admissao",
            "ativo",
            "filial",
            "pj_complementos",
            "user",
        )
        depth = 1


class FuncionariosSimplesSerializer(serializers.ModelSerializer):
    user = UsuariosSimplesSerializer()

    class Meta:
        model = Funcionarios
        fields = (
            "id",
            "nome",
            "user",
        )
        depth = 1
