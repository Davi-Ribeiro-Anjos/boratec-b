from rest_framework import serializers

from usuarios_complementos.serializers import UsuariosSimplesSerializer
from filiais.serializers import FiliaisSimplesSerializer

from .models import Clientes, ClientesFiliais


class ClientesSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = (
            "id",
            "razao_social_motorista",
            "cnpj_cpf",
        )


class ClientesFiliaisSerializer(serializers.ModelSerializer):
    filial = FiliaisSimplesSerializer()
    cliente = ClientesSimplesSerializer()

    class Meta:
        model = ClientesFiliais
        fields = ("id", "filial", "cliente", "saldo", "tipo_palete")
        delth = 1


class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = (
            "id",
            "razao_social_motorista",
            "cnpj_cpf",
            "observacao",
            "tipo_cadastro",
            "autor",
            "filiais",
        )


class ClientesResponseSerializer(serializers.ModelSerializer):
    autor = UsuariosSimplesSerializer()
    # filiais = ClientesFiliaisSerializer(many=True, read_only=True)

    class Meta:
        model = Clientes
        fields = (
            "id",
            "razao_social_motorista",
            "cnpj_cpf",
            "observacao",
            "tipo_cadastro",
            "autor",
            "filiais",
        )
        delth = 1
