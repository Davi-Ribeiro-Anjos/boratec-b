from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer

from .models import PJThirteenths


class PJThirteenthsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PJThirteenths
        fields = (
            "id",
            "months",
            "date_payment",
            "value",
            "send",
            "type_payment",
            "employee",
            "author",
        )


class PJThirteenthsResponseSerializer(serializers.ModelSerializer):
    employee = EmployeesSimpleSerializer()
    date_payment = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = PJThirteenths
        fields = (
            "id",
            "months",
            "date_payment",
            "value",
            "send",
            "type_payment",
            "employee",
        )
        depth = 1
