from rest_framework import serializers

from branches.serializers import BranchesSimpleSerializer

from .models import Routes


class RoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = (
            "id",
            "uf_name",
            "lead_time",
            "temperature",
            "company",
            "boarding",
            "minimum_weight",
            "price_per_kilogram_1",
            "price_per_kilogram_2",
            "price_per_kilogram_3",
            "delivery_fee",
            "ad_valorem",
            "origin",
        )


class RoutesResponseSerializer(serializers.ModelSerializer):
    origin = BranchesSimpleSerializer()

    class Meta:
        model = Routes
        fields = (
            "id",
            "uf_name",
            "lead_time",
            "temperature",
            "company",
            "boarding",
            "minimum_weight",
            "price_per_kilogram_1",
            "price_per_kilogram_2",
            "price_per_kilogram_3",
            "delivery_fee",
            "ad_valorem",
            "origin",
        )
