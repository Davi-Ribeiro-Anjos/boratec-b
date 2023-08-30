from rest_framework import serializers

from epis_sizes.serializers import (
    EPIsSizesSimpleSerializer,
    EPIsSizesRequestsSerializer,
)

# from epis_requests.serializers import EPIsRequestsSimpleSerializer


from .models import EPIsCarts


class EPIsCartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPIsCarts
        fields = ("id", "quantity", "size", "request")


class EPIsCartsResponseSerializer(serializers.ModelSerializer):
    # size = EPIsSizesSimpleSerializer()
    # request = EPIsRequestsSimpleSerializer()

    class Meta:
        model = EPIsCarts
        fields = (
            "id",
            "quantity",
            "size",
            "request",
        )
        depth = 1


class EPIsCartsSimpleSerializer(serializers.ModelSerializer):
    size = EPIsSizesSimpleSerializer()

    class Meta:
        model = EPIsCarts
        fields = (
            "id",
            "quantity",
            "size",
        )
        depth = 1


class EPIsCartsRequestsSerializer(serializers.ModelSerializer):
    size = EPIsSizesRequestsSerializer()

    class Meta:
        model = EPIsCarts
        fields = (
            "id",
            "quantity",
            "size",
        )
        depth = 1
