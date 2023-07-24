from rest_framework import serializers

from usuarios.serializers import UsuariosSimplesSerializer

from .models import PJContratos


class PJContratosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PJContratos
        fields = (
            "id",
            "inicio_contrato",
            "final_contrato",
            "data_reajuste",
            "valor_reajuste",
            "anexo",
            "observacao",
            "data_criacao",
            "autor",
            "funcionario",
        )


class PJContratosResponseSerializer(serializers.ModelSerializer):
    autor = UsuariosSimplesSerializer()
    inicio_contrato = serializers.DateField(format="%d-%m-%Y")
    final_contrato = serializers.DateField(format="%d-%m-%Y")
    data_reajuste = serializers.DateField(format="%d-%m-%Y")
    data_criacao = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = PJContratos
        fields = (
            "id",
            "inicio_contrato",
            "final_contrato",
            "data_reajuste",
            "valor_reajuste",
            "anexo",
            "observacao",
            "data_criacao",
            "autor",
            "funcionario",
        )
        depth = 1
