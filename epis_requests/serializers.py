from rest_framework import serializers

from employees.serializers import EmployeesSimpleSerializer
from branches.serializers import BranchesSimpleSerializer
from epis_carts.models import EPIsCarts
from epis_carts.serializers import EPIsCartsRequestsSerializer

# from epis_items.serializers import EPIsItemsResponseSerializer

from .models import EPIsRequests


class EPIsRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPIsRequests
        fields = (
            "id",
            "date_requested",
            "date_send",
            "date_confirmed",
            "date_canceled",
            "attachment_confirm",
            "status",
            "branch",
            "employee",
            "author_create",
            "author_confirm",
            "author_cancel",
        )


class EPIsRequestsResponseSerializer(serializers.ModelSerializer):
    epis_carts = serializers.SerializerMethodField()
    author_create = EmployeesSimpleSerializer()
    author_confirm = EmployeesSimpleSerializer()
    author_cancel = EmployeesSimpleSerializer()
    employee = EmployeesSimpleSerializer()
    branch = BranchesSimpleSerializer()
    date_requested = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = EPIsRequests
        fields = (
            "id",
            "date_requested",
            "date_send",
            "date_confirmed",
            "date_canceled",
            "attachment_confirm",
            "status",
            "branch",
            "employee",
            "epis_carts",
            "author_create",
            "author_confirm",
            "author_cancel",
        )
        depth = 1

    def get_epis_carts(self, obj):
        epis_carts = EPIsCarts.objects.filter(request=obj)
        serializer = EPIsCartsRequestsSerializer(epis_carts, many=True)

        return serializer.data


class EPIsRequestsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPIsRequests
        fields = (
            "id",
            "date_requested",
            "date_send",
            "date_confirmed",
            "date_canceled",
            "attachment_confirm",
            "status",
            "branch",
            "employee",
            "author_create",
            "author_send",
            "author_confirm",
            "author_cancel",
        )
