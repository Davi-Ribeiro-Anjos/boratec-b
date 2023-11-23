from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Roles
from .serializers import RolesResponseSerializer


class RolesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        vehicles = Roles.objects.filter(active=True).order_by("name")
        serializer = RolesResponseSerializer(vehicles, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
