from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import EPIsSizes
from .serializers import (
    EPIsSizesSerializer,
    EPIsSizesResponseSerializer,
)
from .permissions import BasePermission


class EPIsSizesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        sizes = EPIsSizes.objects.all()

        serializer = EPIsSizesResponseSerializer(sizes, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = EPIsSizesSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        size = EPIsSizes.objects.create(**serializer.validated_data)

        serializer = EPIsSizesResponseSerializer(size)

        return Response(serializer.data, status.HTTP_201_CREATED)
