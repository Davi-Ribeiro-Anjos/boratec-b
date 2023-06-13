from rest_framework import serializers

from usuarios_complementos.serializers import UsuariosSimplesSerializer

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
    autor = UsuariosSimplesSerializer()

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
