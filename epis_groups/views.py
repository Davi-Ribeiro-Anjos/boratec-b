from datetime import date

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from vehicles.models import Vehicles

from .models import EPIsGroups
from .serializers import (
    EPIsGroupsSerializer,
    EPIsGroupsResponseSerializer,
)
from .permissions import BasePermission


class EPIsGroupsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        groups = EPIsGroups.objects.all()

        serializer = EPIsGroupsResponseSerializer(groups, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = EPIsGroupsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        group = EPIsGroups.objects.create(**serializer.validated_data)

        serializer = EPIsGroupsResponseSerializer(group)

        return Response(serializer.data, status.HTTP_201_CREATED)
