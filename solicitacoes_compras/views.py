from rest_framework.views import APIView, Response, Request, status
from django.shortcuts import get_object_or_404

from filiais.models import Filiais
from service.choices import (
    STATUS_CHOICES,
    CATEGORIA_CHOICES,
    DEPARTAMENTO_CHOICES,
    FORMA_PGT_CHOICES,
)

from .models import SolicitacoesCompras
from .serializers import (
    SolicitacoesComprasSerializer,
    SolicitacoesComprasReponseSerializer,
)


class SolicitacoesComprasView(APIView):
    def get(self, request: Request) -> Response:
        solicitacoes = SolicitacoesCompras.objects.all().order_by("id")
        serializer = SolicitacoesComprasReponseSerializer(solicitacoes, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = SolicitacoesComprasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        solicitacao = SolicitacoesCompras.objects.create(**serializer.validated_data)

        serializer = SolicitacoesComprasReponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_201_CREATED)


class SolicitacoesComprasDetailView(APIView):
    def get(self, request: Request, id: int) -> Response:
        solicitacao = get_object_or_404(SolicitacoesCompras, id=id)
        sereliazer = SolicitacoesComprasReponseSerializer(solicitacao)

        return Response(sereliazer.data, status.HTTP_200_OK)


class SolicitacoesComprasChoicesView(APIView):
    def get(self, request: Request) -> Response:
        status_choices = STATUS_CHOICES.choices
        categorias_choices = CATEGORIA_CHOICES.choices
        departamentos_choices = DEPARTAMENTO_CHOICES.choices
        formas_pgt_choices = FORMA_PGT_CHOICES.choices

        choices = [
            {"status": status_choices},
            {"categorias": categorias_choices},
            {"departamentos": departamentos_choices},
            {"formas_pgt": formas_pgt_choices},
        ]

        return Response(choices, status.HTTP_200_OK)
