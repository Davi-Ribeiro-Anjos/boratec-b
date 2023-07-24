from rest_framework import serializers

from funcionarios.serializers import FuncionariosSimplesSerializer

from .models import PaletesControles


class PaletesControlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaletesControles
        fields = [
            "id",
            "localizacao_atual",
            "tipo_palete",
            "movimento_atual",
            "autor",
        ]


class PaletesControlesResponseSerializer(serializers.ModelSerializer):
    autor = FuncionariosSimplesSerializer()

    class Meta:
        model = PaletesControles
        fields = [
            "id",
            "localizacao_atual",
            "tipo_palete",
            "movimento_atual",
            "autor",
        ]
        delth = 1
