from rest_framework import serializers

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
            "author_responsible",
            "branch_issuing",
            "branch_destination",
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
            "weight",
            "opened",
            "nf",
            "occurrences",
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


class DeliveriesHistoriesResponseConfirmedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveriesHistories
        fields = (
            "id",
            "cte",
            "description_justification",
            "file",
            "nf",
        )


class DeliveriesHistoriesConsultSerializer(serializers.ModelSerializer):
    lead_time = serializers.DateField(format="%d/%m/%Y")
    date_emission = serializers.DateField(format="%d/%m/%Y")
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
        )
