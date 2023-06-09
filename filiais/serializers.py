from rest_framework import serializers

from .models import Filiais


class FiliaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiais
        fields = [
            "id",
            "id_empresa",
            "id_filial",
            "id_garagem",
            "sigla",
            "nome",
            "uf",
            "cnpj",
        ]


class FiliaisSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiais
        fields = [
            "id",
            "id_garagem",
            "sigla",
        ]
