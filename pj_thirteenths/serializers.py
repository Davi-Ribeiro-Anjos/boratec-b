from rest_framework import serializers

from .models import PJComplements


class PJComplementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PJComplements
        fields = (
            "id",
            "salary",
            "allowance",
            "college",
            "covenant_credit",
            "housing_allowance",
            "others_credits",
            "advance_money",
            "covenant_discount",
            "others_discounts",
            "observation",
            "data_emission",
        )


class PJComplementsResponseSerializer(serializers.ModelSerializer):
    data_emission = serializers.DateTimeField(format="%d/%m/%Y")
    total = serializers.SerializerMethodField()

    class Meta:
        model = PJComplements
        fields = (
            "id",
            "salary",
            "college",
            "allowance",
            "covenant_credit",
            "housing_allowance",
            "others_credits",
            "advance_money",
            "covenant_discount",
            "others_discounts",
            "data_emission",
            "observation",
            "total",
        )
        depth = 1

    def get_total(self, obj):
        return (
            obj.salary
            + obj.allowance
            + obj.college
            + obj.covenant_credit
            + obj.others_credits
            + obj.housing_allowance
            - obj.advance_money
            - obj.covenant_discount
            - obj.others_discounts
        )
