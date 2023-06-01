from rest_framework.views import APIView, Response, Request, status
from django.shortcuts import get_object_or_404

from .models import SolicitacoesEntradas
from .serializers import (
    SolicitacoesEntradasSerializer,
    SolicitacoesEntradasReponseSerializer,
)


class SolicitacoesEntradasView(APIView):
    def get(self, request: Request) -> Response:
        solicitacoes = SolicitacoesEntradas.objects.all().order_by("id")
        serializer = SolicitacoesEntradasReponseSerializer(solicitacoes, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = SolicitacoesEntradasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        solicitacao = SolicitacoesEntradas.objects.create(**serializer.validated_data)

        serializer = SolicitacoesEntradasReponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_201_CREATED)


class SolicitacoesEntradasDetailView(APIView):
    def get(self, request: Request, id: int) -> Response:
        solicitacao = SolicitacoesEntradas.objects.filter(solicitacao__id=id).order_by(
            "id"
        )
        serializer = SolicitacoesEntradasReponseSerializer(solicitacao, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, id: int) -> Response:
        solicitacao = get_object_or_404(SolicitacoesEntradas, id=id)
        serializer = SolicitacoesEntradasSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(solicitacao, key, value)

        solicitacao.save()

        serializer = SolicitacoesEntradasReponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_201_CREATED)
