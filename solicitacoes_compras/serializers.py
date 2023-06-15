from rest_framework import serializers

from filiais.serializers import FiliaisSimplesSerializer
from usuarios_complementos.serializers import UsuariosSimplesSerializer

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


class SolicitacoesComprasSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitacoesCompras
        fields = (
            "id",
            "numero_solicitacao",
            "data_solicitacao_bo",
            "data_vencimento_boleto",
            "data_conclusao_pedido",
            "status",
            "observacao",
        )


class SolicitacoesComprasResponseSerializer(serializers.ModelSerializer):
    filial = FiliaisSimplesSerializer()
    solicitante = UsuariosSimplesSerializer()
    responsavel = UsuariosSimplesSerializer()
    autor = UsuariosSimplesSerializer()
    ultima_atualizacao = UsuariosSimplesSerializer()
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


class SolicitacoesComprasEditarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitacoesCompras
        fields = (
            "numero_solicitacao",
            "data_vencimento_boleto",
            "data_conclusao_pedido",
            "status",
            "departamento",
            "categoria",
            "forma_pagamento",
            "pago",
            "observacao",
            "anexo",
            "responsavel",
            "ultima_atualizacao",
        )
