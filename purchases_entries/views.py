from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404

from .models import PurchasesEntries
from .serializers import (
    PurchasesEntriesSerializer,
    PurchasesEntriesResponseSerializer,
)
from .permissions import BasePermission, DetailsPermission


class PurchasesEntriesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        solicitations = PurchasesEntries.objects.all().order_by("id")
        serializer = PurchasesEntriesResponseSerializer(solicitations, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = PurchasesEntriesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        solicitation = PurchasesEntries.objects.create(**serializer.validated_data)

        serializer = PurchasesEntriesResponseSerializer(solicitation)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PurchasesEntriesDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, DetailsPermission]

    def get(self, request: Request, id: int) -> Response:
        solicitation = PurchasesEntries.objects.filter(request__id=id).order_by("id")
        serializer = PurchasesEntriesResponseSerializer(solicitation, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    # def patch(self, request: Request, id: int) -> Response:
    #     solicitation = get_object_or_404(PurchasesEntries, id=id)

    #     serializer = PurchasesEntriesSerializer(data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)

    #     for key, value in serializer.validated_data.items():
    #         setattr(solicitation, key, value)

    #     solicitation.save()

    #     serializer = PurchasesEntriesResponseSerializer(solicitation)

    #     return Response(serializer.data, status.HTTP_201_CREATED)
