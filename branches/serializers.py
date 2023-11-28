from rest_framework import serializers

from branches.models import Branches


class BranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = [
            "id",
            "id_company",
            "id_branch",
            "id_garage",
            "abbreviation",
            "name",
            "uf",
            "cnpj",
        ]


class BStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = [
            "id",
            "abbreviation",
            "name",
            "uf",
            "company",
        ]


class BranchesSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = [
            "id",
            "id_garage",
            "abbreviation",
        ]
