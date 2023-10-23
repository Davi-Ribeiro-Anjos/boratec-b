import ipdb

from datetime import date, datetime, timedelta

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
        today = date.today()

        try:
            data = request.data.dict()
        except:
            data = request.data

        try:
            difference_date = (
                datetime.strptime(data["date_release"], "%Y-%m-%d").date() - today
            )
        except Exception:
            try:
                difference_date = (
                    datetime.strptime(data["date_forecast"], "%Y-%m-%d").date() - today
                )
            except:
                difference_date = None

        vehicle = Vehicles.objects.get(id=data["vehicle"])

        if vehicle.last_movement:
            fleet = FleetsAvailabilities.objects.get(id=vehicle.last_movement)

            if fleet.date_forecast and today <= fleet.date_forecast:
                fleets = FleetsAvailabilities.objects.filter(
                    vehicle=vehicle.id, date_occurrence__gte=today
                )
            elif fleet.date_release and today <= fleet.date_release:
                fleets = FleetsAvailabilities.objects.filter(
                    vehicle=vehicle.id, date_occurrence_gte=today
                )
            else:
                fleets = None

            if fleets:
                fleets.delete()

        if difference_date:
            for number in range(0, difference_date.days + 1):
                provisory_date = today + timedelta(days=number)

                if "date_forecast" in data or "date_release" in data:
                    data["date_occurrence"] = provisory_date

                print(data["date_occurrence"])
                print(data)

                serializer = FleetsAvailabilitiesSerializer(data=data)
                serializer.is_valid(raise_exception=True)

                if number == 0:
                    availability = FleetsAvailabilities.objects.create(
                        **serializer.validated_data
                    )
                else:
                    FleetsAvailabilities.objects.create(**serializer.validated_data)

        else:
            serializer = FleetsAvailabilitiesSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            availability = FleetsAvailabilities.objects.create(
                **serializer.validated_data
            )

        vehicle.last_movement = availability.id
        vehicle.save()

        serializer = FleetsAvailabilitiesResponseSerializer(availability)

        return Response(serializer.data, status.HTTP_201_CREATED)
