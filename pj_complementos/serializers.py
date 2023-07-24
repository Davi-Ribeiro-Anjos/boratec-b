from rest_framework import serializers

from .models import PJComplementos


class PJComplementosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PJComplementos
        fields = (
            "id",
            "salario",
            "ajuda_custo",
            "faculdade",
            "credito_convenio",
            "auxilio_moradia",
            "outros_creditos",
            "adiantamento",
            "desconto_convenio",
            "outros_descontos",
            "data_pagamento",
            "data_emissao",
        )


class PJComplementosResponseSerializer(serializers.ModelSerializer):
    data_pagamento = serializers.DateField(format="%d-%m-%Y")
    data_emissao = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = PJComplementos
        fields = (
            "id",
            "salario",
            "faculdade",
            "ajuda_custo",
            "credito_convenio",
            "auxilio_moradia",
            "outros_creditos",
            "adiantamento",
            "desconto_convenio",
            "outros_descontos",
            "data_pagamento",
            "data_emissao",
        )
        depth = 1
