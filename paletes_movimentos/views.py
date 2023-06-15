from rest_framework.views import APIView, Response, Request, status

from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404

import ipdb
from datetime import datetime

from filiais.models import Filiais
from paletes_controles.models import PaletesControles

from .models import PaletesMovimentos
from .serializers import *


class PaletesMovimentosView(APIView):
    def get(self, request: Request) -> Response:
        params = request.GET.dict()

        print(params)

        lista_params = [
            "origem",
            "destino",
            "placa_veiculo",
            "placa_veiculo__contains",
            "autor",
            "autor__username",
            "recebido",
        ]

        params_errados = [param for param in params if not param in lista_params]
        if len(params_errados) > 0:
            raise FieldError()

        if "recebido" in params:
            if params["recebido"] == "false":
                params["recebido"] = False
            elif params["recebido"] == "true":
                params["recebido"] = True

        try:
            if params:
                movimentos = PaletesMovimentos.objects.filter(**params).order_by(
                    "data_solicitacao"
                )
                serializer = PaletesMovimentosResponseSerializer(movimentos, many=True)

                return Response(serializer.data, status.HTTP_200_OK)
            else:
                movimentos = PaletesMovimentos.objects.all().order_by(
                    "data_solicitacao"
                )
                serializer = PaletesMovimentosResponseSerializer(movimentos, many=True)

                return Response(serializer.data, status.HTTP_200_OK)
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
        except Exception as e:
            return Response({"error": e}, status.HTTP_400_BAD_REQUEST)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        tempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        solicitacao = (
            str(tempo).replace(":", "").replace(" ", "").replace("-", "")
            + data["placa_veiculo"][5:]
        )

        data = {"solicitacao": solicitacao, **data}

        serializer = PaletesMovimentosSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        filial = Filiais.objects.get(id=data["origem"])

        paletes = PaletesControles.objects.filter(
            localizacao_atual=filial.sigla, movimento_atual__isnull=True
        )

        if paletes.count() < int(data["quantidade_paletes"]):
            return Response(
                {
                    "mensagem": f"A filial {filial.sigla} não tem essa quantidade de paletes disponível"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            movimento: PaletesMovimentos = PaletesMovimentos.objects.create(
                **serializer.validated_data
            )

            for _ in range(0, int(data["quantidade_paletes"])):
                palete = PaletesControles.objects.filter(
                    localizacao_atual=filial.sigla,
                    movimento_atual__isnull=True,
                    tipo_palete=data["tipo_palete"],
                ).first()

                item = {
                    "movimento_atual": movimento.solicitacao,
                    "localizacao_atual": "MOV",
                    "destino": movimento.destino.sigla,
                }

                for key, value in item.items():
                    setattr(palete, key, value)

                palete.save()

            serializer: PaletesMovimentosResponseSerializer = (
                PaletesMovimentosResponseSerializer(movimento)
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaletesMovimentosDetailView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        solicitacao = get_object_or_404(PaletesMovimentos, id=id)
        serializer = PaletesMovimentosSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(solicitacao, key, value)

        try:
            paletes = PaletesControles.objects.filter(
                movimento_atual=solicitacao.solicitacao,
                destino=solicitacao.destino.sigla,
            )

            for palete in paletes:
                palete.localizacao_atual = palete.destino
                palete.destino = None
                palete.movimento_atual = None

                palete.save()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        solicitacao.save()

        serializer = PaletesMovimentosResponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_201_CREATED)
