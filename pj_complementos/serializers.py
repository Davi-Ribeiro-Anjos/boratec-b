from rest_framework import serializers

from usuarios.serializers import UsuariosSimplesSerializer

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
            "autor",
        )


class PJComplementosResponseSerializer(serializers.ModelSerializer):
    autor = UsuariosSimplesSerializer()
    data_pagamento = serializers.DateField(format="%d-%m-%Y")
    data_emissao = serializers.DateTimeField(format="%d-%m-%Y")
    total = serializers.SerializerMethodField()

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
            "autor",
            "total",
        )
        depth = 1

        def get_total(self, obj):
            if obj:
                return (
                    obj.salario
                    + obj.ajuda_custo
                    + obj.faculdade
                    + obj.credito_convenio
                    + obj.outros_creditos
                    + obj.auxilio_moradia
                    - obj.adiantamento
                    - obj.desconto_convenio
                    - obj.outros_descontos
                )
            else:
                return 0
