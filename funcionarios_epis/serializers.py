from rest_framework import serializers

from .models import FuncionariosEPIs


class FuncionariosEpisResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuncionariosEPIs
        fields = (
            "id",
            "celular_modelo",
            "celular_numero_ativo",
            "notebook_modelo",
            "notebook_numero_ativo",
        )
