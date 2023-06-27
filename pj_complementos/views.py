from rest_framework.views import APIView, Response, Request, status

from django.shortcuts import get_object_or_404

from .models import PJComplementos
from .serializers import (
    PJComplementosSerializer,
    PJComplementosSimplesResponseSerializer,
)


class PJComplementosDetailView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        pj_complemento = get_object_or_404(PJComplementos, id=id)
        serializer = PJComplementosSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(pj_complemento, key, value)

        pj_complemento.save()

        serializer = PJComplementosSimplesResponseSerializer(pj_complemento)

        return Response(serializer.data, status.HTTP_201_CREATED)
