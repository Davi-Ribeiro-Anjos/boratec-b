from rest_framework import serializers

from .models import EmployeesEPIs


class EmployeesEPIsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeesEPIs
        fields = (
            "id",
            "phone_model",
            "phone_code",
            "notebook_model",
            "notebook_code",
            "observation",
        )
