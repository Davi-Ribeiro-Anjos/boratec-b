from rest_framework import serializers

from .models import SolicitacoesCompras


class SolicitacoesComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitacoesCompras
        fields = [
            "id",
            "numero_solicitacao",
            "data_solicitacao_pra",
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
        ]
