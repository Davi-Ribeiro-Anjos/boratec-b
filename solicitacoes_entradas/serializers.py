from rest_framework import serializers

from solicitacoes_compras.serializers import SolicitacoesComprasReponseSerializer
from usuarios.serializers import UsuariosSerializer

from .models import SolicitacoesEntradas


class SolicitacoesEntradasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitacoesEntradas
        fields = (
            "id",
            "obs",
            "arquivo_1",
            "arquivo_2",
            "arquivo_3",
            "data_criacao",
            "solicitacao",
            "autor",
        )


class SolicitacoesEntradasReponseSerializer(serializers.ModelSerializer):
    autor = UsuariosSerializer()

    class Meta:
        model = SolicitacoesEntradas
        fields = (
            "id",
            "obs",
            "arquivo_1",
            "arquivo_2",
            "arquivo_3",
            "data_criacao",
            "solicitacao",
            "autor",
        )
        depth = 1
