from datetime import datetime
from rest_framework.views import APIView, Response, Request, status

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from filiais.models import Filiais
from paletes_controles.models import PaletesControles

from .models import PaletesMovimentos
from .serializers import *


class PaletesMovimentosView(APIView):
    def get(self, request: Request) -> Response:
        movimentos = PaletesMovimentos.objects.all().order_by("id")
        serializer = PaletesMovimentosResponseSerializer(movimentos, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

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

            serializer: PaletesMovimentosResponseSerializer = (
                PaletesMovimentosResponseSerializer(movimento)
            )

            for _ in range(0, int(data["quantidade_paletes"])):
                palete = PaletesControles.objects.filter(
                    localizacao_atual=filial.sigla, movimento_atual__isnull=True
                ).first()

                item = {
                    "movimento_atual": movimento.solicitacao,
                    "localizacao_atual": "MOV",
                }

                for key, value in item.items():
                    setattr(palete, key, value)

                palete.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaletesMovimentosDetailView(APIView):
    def get(self, request: Request, id: int) -> Response:
        solicitacao = PaletesMovimentos.objects.filter(solicitacao__id=id).order_by(
            "id"
        )
        serializer = PaletesMovimentosResponseSerializer(solicitacao, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, id: int) -> Response:
        solicitacao = get_object_or_404(PaletesMovimentos, id=id)
        serializer = PaletesMovimentosSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(solicitacao, key, value)

        solicitacao.save()

        serializer = PaletesMovimentosResponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_201_CREATED)
