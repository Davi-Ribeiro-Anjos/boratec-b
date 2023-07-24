from rest_framework import serializers

from filiais.serializers import FiliaisSimplesSerializer
from funcionarios.serializers import FuncionariosSimplesSerializer

from .models import PaletesMovimentos


class PaletesMovimentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaletesMovimentos
        fields = (
            "id",
            "solicitacao",
            "data_solicitacao",
            "data_recebimento",
            "placa_veiculo",
            "motorista",
            "conferente",
            "recebido",
            "quantidade_paletes",
            "origem",
            "destino",
            "autor",
        )


class PaletesMovimentosSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaletesMovimentos
        fields = (
            "id",
            "solicitacao",
            "data_solicitacao",
            "data_recebimento",
            "placa_veiculo",
            "motorista",
            "conferente",
            "recebido",
            "quantidade_paletes",
            "origem",
            "destino",
            "autor",
        )


class PaletesMovimentosResponseSerializer(serializers.ModelSerializer):
    origem = FiliaisSimplesSerializer()
    destino = FiliaisSimplesSerializer()
    autor = FuncionariosSimplesSerializer()
    data_solicitacao = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    data_recebimento = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = PaletesMovimentos
        fields = (
            "id",
            "solicitacao",
            "data_solicitacao",
            "data_recebimento",
            "placa_veiculo",
            "motorista",
            "conferente",
            "quantidade_paletes",
            "recebido",
            "origem",
            "destino",
            "autor",
        )
        depth = 1
