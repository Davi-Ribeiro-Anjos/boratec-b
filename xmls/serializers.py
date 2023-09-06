from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer


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
    date_emission = serializers.DateField(format="%d/%m/%Y")
    date_published = serializers.DateField(format="%d/%m/%Y")
    author = EmployeesSimpleSerializer()

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
        depth = 1


class XmlsSimpleSerializer(serializers.ModelSerializer):
    epis_sizes = serializers.SerializerMethodField()
    validity = serializers.DateField(format="%d/%m/%Y")

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
        depth = 1
