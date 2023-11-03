from rest_framework import serializers

from .models import Occurrences


class OccurrencesRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occurrences
        fields = (
            "id",
            "cte",
            "garage",
            "date_emission",
            "document_type",
            "occurrence_code",
            "occurrence_description",
            "justification",
            "branch",
        )


class OccurrencesResponseSerializer(serializers.ModelSerializer):
    date_emission = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Occurrences
        fields = (
            "id",
            "date_emission",
            "document_type",
            "occurrence_code",
            "occurrence_description",
            "justification",
            "branch",
        )


class OccurrencesSimpleSerializer(serializers.ModelSerializer):
    date_emission = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Occurrences
        fields = (
            "date_emission",
            "occurrence_description",
        )
