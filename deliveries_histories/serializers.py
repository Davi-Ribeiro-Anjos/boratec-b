from rest_framework import serializers

from branches.serializers import BStatusSerializer, BranchesSimpleSerializer

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
    date_emission = serializers.DateField(format="%d/%m/%Y")
    lead_time = serializers.DateField(format="%d/%m/%Y")
    date_delivery = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = DeliveriesHistories
        fields = (
            "id",
            "cte",
            "description_justification",
            "file",
            "nf",
            "date_emission",
            "lead_time",
            "date_delivery",
        )


class DeliveriesHistoriesPerformancesSerializer(serializers.ModelSerializer):
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


class DHStatusSerializer(serializers.ModelSerializer):
    date_emission = serializers.DateField(format="%d/%m/%Y")
    lead_time = serializers.DateField(format="%d/%m/%Y")
    date_delivery = serializers.DateField(format="%d/%m/%Y")
    branch_issuing = BranchesSimpleSerializer()
    branch_destination = BStatusSerializer()
    last_occurrence = serializers.SerializerMethodField()

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
            "nf",
            "branch_issuing",
            "branch_destination",
            "last_occurrence",
        )

    def get_last_occurrence(self, obj):
        from occurrences.models import Occurrences
        from occurrences.serializers import (
            OccurrencesSimpleSerializer,
        )

        occurrence = (
            Occurrences.objects.filter(
                justification=obj.id, occurrence_description="Entregue"
            )
            .order_by("date_emission")
            .first()
        )

        if not occurrence:
            occurrence = (
                Occurrences.objects.filter(justification=obj.id)
                .order_by("date_emission")
                .last()
            )

        if occurrence:
            serializer = OccurrencesSimpleSerializer(occurrence)

            return serializer.data

        return None
