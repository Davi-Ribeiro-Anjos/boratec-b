from rest_framework import serializers

from users.serializers import UserSimpleSerializer


from .models import Xmls


class XmlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xmls
        fields = (
            "id",
            "date_emission",
            "nf",
            "sender",
            "recipient",
            "weight",
            "volume",
            "value_nf",
            "district",
            "cep",
            "county",
            "uf",
            "printed",
            "date_published",
            "xml_file",
            "author",
        )


class XmlsResponseSerializer(serializers.ModelSerializer):
    date_emission = serializers.DateTimeField(format="%d/%m/%Y")
    date_published = serializers.DateTimeField(format="%d/%m/%Y")
    author = UserSimpleSerializer()

    class Meta:
        model = Xmls
        fields = (
            "id",
            "date_emission",
            "nf",
            "sender",
            "recipient",
            "weight",
            "volume",
            "value_nf",
            "uf",
            "date_published",
            "xml_file",
            "author",
        )
        depth = 1


class XmlsSimpleSerializer(serializers.ModelSerializer):
    date_emission = serializers.DateTimeField(format="%d/%m/%Y")
    date_published = serializers.DateTimeField(format="%d/%m/%Y")
    author = UserSimpleSerializer()

    class Meta:
        model = Xmls
        fields = (
            "id",
            "date_emission",
            "nf",
            "sender",
            "recipient",
            "weight",
            "volume",
            "value_nf",
            "uf",
            "date_published",
            "xml_file",
            "author",
        )
        depth = 1
