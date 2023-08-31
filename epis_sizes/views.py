from django.shortcuts import get_object_or_404
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


class EPIsSizesDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def patch(self, request: Request, id: int) -> Response:
        size = get_object_or_404(EPIsSizes, id=id)

        serializer = EPIsSizesSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        old_size = size.quantity

        for key, value in serializer.validated_data.items():
            setattr(size, key, value)

        size.quantity_provisory = size.quantity_provisory + (size.quantity - old_size)
        print(size.quantity_provisory)

        if size.quantity_provisory < 0:
            return Response(
                {"message": "Insira um valor maior em Quantidade"},
                status.HTTP_400_BAD_REQUEST,
            )

        size.save()

        serializer = EPIsSizesResponseSerializer(size)

        return Response(serializer.data, status.HTTP_201_CREATED)
