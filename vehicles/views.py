from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Vehicles
from .serializers import VehiclesResponseSerializer
from .permissions import BasePermission


class VehiclesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        vehicles = Vehicles.objects.filter(**filter).order_by("vehicle_plate")
        serializer = VehiclesResponseSerializer(vehicles, many=True)

        total_vehicles = vehicles.count()

        response_data = {
            "total": total_vehicles,
            "data": serializer.data,
        }

        return Response(response_data, status.HTTP_200_OK)
