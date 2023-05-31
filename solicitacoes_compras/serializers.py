from rest_framework import serializers

from filiais.serializers import FiliaisSerializer
from usuarios.serializers import UsuariosSerializer

from .models import SolicitacoesCompras


class SolicitacoesComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitacoesCompras
        fields = (
            "id",
            "numero_solicitacao",
            "data_solicitacao_bo",
            "data_vencimento_boleto",
            "data_conclusao_pedido",
            "status",
            "departamento",
            "categoria",
            "forma_pagamento",
            "pago",
            "observacao",
            "anexo",
            "filial",
            "solicitante",
            "responsavel",
            "autor",
            "ultima_atualizacao",
        )


class SolicitacoesComprasReponseSerializer(serializers.ModelSerializer):
    filial = FiliaisSerializer()
    solicitante = UsuariosSerializer()
    responsavel = UsuariosSerializer()
    autor = UsuariosSerializer()
    ultima_atualizacao = UsuariosSerializer()
    data_solicitacao_bo = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = SolicitacoesCompras
        fields = (
            "id",
            "numero_solicitacao",
            "data_solicitacao_bo",
            "data_vencimento_boleto",
            "data_conclusao_pedido",
            "status",
            "departamento",
            "categoria",
            "forma_pagamento",
            "pago",
            "observacao",
            "anexo",
            "filial",
            "solicitante",
            "responsavel",
            "autor",
            "ultima_atualizacao",
        )
        depth = 1
