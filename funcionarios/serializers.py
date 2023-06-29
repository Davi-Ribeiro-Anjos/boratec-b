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
            "complemento_funcionario",
            "user",
        )


class FuncionariosResponseSerializer(serializers.ModelSerializer):
    filial = FiliaisSimplesSerializer()
    complemento_funcionario = PJComplementosResponseSerializer()
    user = UsuariosSimplesSerializer()
    cpf = CPFFormattedField()
    cnpj = CNPJFormattedField()
    total = serializers.SerializerMethodField()

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
            "complemento_funcionario",
            "total",
            "user",
        )
        depth = 1

    def get_total(self, obj):
        return (
            obj.complemento_funcionario.salario
            + obj.complemento_funcionario.ajuda_custo
            + obj.complemento_funcionario.faculdade
            + obj.complemento_funcionario.credito_convenio
            + obj.complemento_funcionario.outros_creditos
            + obj.complemento_funcionario.auxilio_moradia
            - obj.complemento_funcionario.adiantamento
            - obj.complemento_funcionario.desconto_convenio
            - obj.complemento_funcionario.outros_descontos
        )
