import ipdb

from rest_framework.views import APIView, Response, Request, status

from django.db.models import Q
from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404

from .models import (
    SolicitacoesCompras,
    STATUS_CHOICES,
    CATEGORIA_CHOICES,
    DEPARTAMENTO_CHOICES,
    FORMA_PGT_CHOICES,
)
from .serializers import *


class SolicitacoesComprasView(APIView):
    def get(self, request: Request) -> Response:
        params = request.GET.dict()
        lista_params = [
            "numero_solicitacao",
            "data_solicitacao_bo",
            "data_solicitacao_bo__gte",
            "data_solicitacao_bo__lte",
            "solicitante",
            "solicitante__username",
            "status",
            "filial",
        ]

        params_errados = [param for param in params if not param in lista_params]
        if len(params_errados) > 0:
            raise FieldError()

        try:
            if len(request.GET) > 0:
                if not "status" in params:
                    params["status__in"] = ["ABERTO", "ANDAMENTO"]
                    solicitacoes = SolicitacoesCompras.objects.filter(
                        **params
                    ).order_by("data_solicitacao_bo")

                solicitacoes = SolicitacoesCompras.objects.filter(**params).order_by(
                    "data_solicitacao_bo"
                )
            else:
                solicitacoes = SolicitacoesCompras.objects.filter(
                    Q(status="ABERTO") | Q(status="ANDAMENTO")
                ).order_by("data_solicitacao_bo")
        except FieldError:
            return Response(
                {
                    "mensagem": "Parâmetros incorrretos",
                    "parametros_aceitos": [
                        "numero_solicitacao",
                        "data_solicitacao_bo",
                        "status",
                        "solicitante",
                        "filial",
                    ],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SolicitacoesComprasResponseSerializer(solicitacoes, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = SolicitacoesComprasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        solicitacao = SolicitacoesCompras.objects.create(**serializer.validated_data)

        serializer = SolicitacoesComprasResponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_201_CREATED)


class SolicitacoesComprasDetailView(APIView):
    def get(self, request: Request, id: int) -> Response:
        solicitacao = get_object_or_404(SolicitacoesCompras, id=id)
        serializer = SolicitacoesComprasResponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, id: int) -> Response:
        solicitacao = get_object_or_404(SolicitacoesCompras, id=id)
        serializer = SolicitacoesComprasSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(solicitacao, key, value)

        solicitacao.save()

        serializer = SolicitacoesComprasResponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_204_NO_CONTENT)


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
