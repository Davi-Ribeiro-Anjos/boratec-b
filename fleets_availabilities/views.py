from rest_framework.views import APIView, Response, Request, status

from .models import FleetsAvailabilities
from .serializers import FleetsAvailabilitiesResponseSerializer


class FleetsAvailabilitiesView(APIView):
    def get(self, request: Request) -> Response:
        fleet = FleetsAvailabilities.objects.all()
        serializer = FleetsAvailabilitiesResponseSerializer(fleet, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
