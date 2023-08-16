from rest_framework import serializers

from .models import EmployeesDismissals


class EmployeesDismissalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeesDismissals
        fields = (
            "id",
            "dismissal_date",
            "dismissal_motive",
        )
