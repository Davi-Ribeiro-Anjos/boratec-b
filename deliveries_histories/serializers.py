from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer
from branches.serializers import BranchesSimpleSerializer
from epis_carts.models import EPIsCarts
from epis_carts.serializers import EPIsCartsRequestsSerializer

# from epis_items.serializers import EPIsItemsResponseSerializer

from .models import DeliveriesHistories


class DeliveriesHistoriesRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveriesHistories
        fields = (
            "id",
            "cte",
            "date_emission",
            "lead_time",
            "date_delivery",
            "recipient",
            "sender",
            "delivery_location",
            "weight",
            "opened",
            "nf",
            "document_type",
            "description_justification",
            "file",
            "confirmed",
            "refuse",
            "author",
            "branch",
        )


class DeliveriesHistoriesResponseSerializer(serializers.ModelSerializer):
    occurrences = serializers.SerializerMethodField()
    date_emission = serializers.DateField(format="%d/%m/%Y")
    lead_time = serializers.DateField(format="%d/%m/%Y")
    date_delivery = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = DeliveriesHistories
        fields = (
            "id",
            "cte",
            "date_emission",
            "lead_time",
            "date_delivery",
            "recipient",
            "sender",
            "delivery_location",
            "weight",
            "opened",
            "nf",
            "document_type",
            "description_justification",
            "file",
            "confirmed",
            "refuse",
            "occurrences",
            "author",
            "branch",
        )

    def get_occurrences(self, obj):
        from occurrences.models import Occurrences
        from occurrences.serializers import (
            OccurrencesSimpleSerializer,
        )

        occurrences = Occurrences.objects.filter(justification=obj.id)

        if occurrences:
            serializer = OccurrencesSimpleSerializer(occurrences, many=True)

            return serializer.data

        return None
