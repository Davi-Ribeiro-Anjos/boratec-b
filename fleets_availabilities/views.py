from datetime import date

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from vehicles.models import Vehicles

from .models import FleetsAvailabilities
from .serializers import (
    FleetsAvailabilitiesSerializer,
    FleetsAvailabilitiesResponseSerializer,
)
from .permissions import BasePermission


class FleetsAvailabilitiesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        fleet = FleetsAvailabilities.objects.all()

        serializer = FleetsAvailabilitiesResponseSerializer(fleet, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = FleetsAvailabilitiesSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        solicitation = FleetsAvailabilities.objects.create(**serializer.validated_data)

        vehicle = Vehicles.objects.get(id=data["vehicle"])

        vehicle.last_movement = vehicle.id
        vehicle.save()

        serializer = FleetsAvailabilitiesResponseSerializer(solicitation)

        return Response(serializer.data, status.HTTP_201_CREATED)
