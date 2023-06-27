from rest_framework import serializers

from solicitacoes_compras.serializers import SolicitacoesComprasSimplesSerializer
from usuarios.serializers import UsuariosSimplesSerializer

from .models import SolicitacoesEntradas


class SolicitacoesEntradasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitacoesEntradas
        fields = (
            "id",
            "observacao",
            "arquivo_1",
            "arquivo_2",
            "arquivo_3",
            "data_criacao",
            "solicitacao",
            "autor",
        )


class SolicitacoesEntradasResponseSerializer(serializers.ModelSerializer):
    autor = UsuariosSimplesSerializer()
    solicitacao = SolicitacoesComprasSimplesSerializer()

    class Meta:
        model = SolicitacoesEntradas
        fields = (
            "id",
            "observacao",
            "arquivo_1",
            "arquivo_2",
            "arquivo_3",
            "data_criacao",
            "solicitacao",
            "autor",
        )
        depth = 1
