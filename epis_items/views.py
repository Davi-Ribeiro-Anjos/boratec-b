from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import EPIsItems
from .serializers import (
    EPIsItemsSerializer,
    EPIsItemsResponseSerializer,
)
from .permissions import BasePermission


class EPIsItemsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        items = EPIsItems.objects.all()

        serializer = EPIsItemsResponseSerializer(items, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = EPIsItemsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        item = EPIsItems.objects.create(**serializer.validated_data)

        serializer = EPIsItemsResponseSerializer(item)

        return Response(serializer.data, status.HTTP_201_CREATED)
