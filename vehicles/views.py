from rest_framework.views import APIView, Response, Request, status

from .models import Vehicles
from .serializers import VehiclesResponseSerializer


class VehiclesView(APIView):
    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        vehicles = Vehicles.objects.filter(**filter).order_by("vehicle_plate")
        serializer = VehiclesResponseSerializer(vehicles, many=True)

        total_vehicles = vehicles.count()  # Contagem total de objetos após o filtro

        serializer = VehiclesResponseSerializer(vehicles, many=True)
        response_data = {
            "total": total_vehicles,  # Adiciona o campo 'total' ao dicionário de resposta
            "data": serializer.data,
        }

        return Response(response_data, status.HTTP_200_OK)
