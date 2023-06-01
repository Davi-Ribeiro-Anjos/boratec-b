import ipdb
from rest_framework.views import APIView, Response, Request, status
from django.db.models import Q
from django.shortcuts import get_object_or_404

from filiais.models import Filiais
from _service.choices import (
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
        if len(request.GET) > 0:
            solicitacoes = SolicitacoesCompras.objects.filter(
                **request.GET.dict()
            ).order_by("data_solicitacao_bo")
        else:
            solicitacoes = SolicitacoesCompras.objects.filter(
                Q(status="ABERTO") | Q(status="ANDAMENTO")
            ).order_by("data_solicitacao_bo")

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
        serializer = SolicitacoesComprasReponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, id: int) -> Response:
        solicitacao = get_object_or_404(SolicitacoesCompras, id=id)
        serializer = SolicitacoesComprasSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(solicitacao, key, value)

        solicitacao.save()

        serializer = SolicitacoesComprasReponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_201_CREATED)


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
