from rest_framework.views import APIView, Response, Request, status

from django.shortcuts import get_object_or_404

from .models import PJContratos
from .serializers import (
    PJContratosSerializer,
    PJContratosResponseSerializer,
)


class PJContratosView(APIView):
    def get(self, request: Request) -> Response:
        pj_contratos = PJContratos.objects.all()

        serializer = PJContratosResponseSerializer(pj_contratos, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = PJContratosSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        pj_contratos = PJContratos.objects.create(**serializer.validated_data)

        serializer = PJContratosResponseSerializer(pj_contratos)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PJContratosDetailView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        pj_cotrato = get_object_or_404(PJContratos, id=id)
        serializer = PJContratosSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(pj_cotrato, key, value)

        pj_cotrato.save()

        serializer = PJContratosResponseSerializer(pj_cotrato)

        return Response(serializer.data, status.HTTP_201_CREATED)
