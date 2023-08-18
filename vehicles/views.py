from rest_framework.views import APIView, Response, Request, status

from .models import Vehicles
from .serializers import VehiclesResponseSerializer


class VehiclesView(APIView):
    def get(self, request: Request) -> Response:
        vehicles = Vehicles.objects.all()
        serializer = VehiclesResponseSerializer(vehicles, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
