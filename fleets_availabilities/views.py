from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import FleetsAvailabilities
from .serializers import FleetsAvailabilitiesResponseSerializer
from .permissions import BasePermission


class FleetsAvailabilitiesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        fleet = FleetsAvailabilities.objects.all()
        serializer = FleetsAvailabilitiesResponseSerializer(fleet, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
