from rest_framework.views import APIView, Response, Request, status

from django.contrib.auth.models import User
from django.db.models import Count, Q, ExpressionWrapper, IntegerField
from django.shortcuts import get_object_or_404

from filiais.models import Filiais

from .models import PaletesControles
from .serializers import *


class PaletesControlesView(APIView):
    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        if filter:
            try:
                paletes = PaletesControles.objects.filter(**filter).order_by("id")
            except Exception:
                paletes = PaletesControles.objects.all().order_by("id")

            serializer = PaletesControlesResponseSerializer(paletes, many=True)

            return Response(serializer.data, status.HTTP_200_OK)
        else:
            paletes = (
                PaletesControles.objects.all()
                .values("localizacao_atual")
                .annotate(
                    PBR=Count("id", filter=Q(tipo_palete="PBR")),
                    CHEP=Count("id", filter=Q(tipo_palete="CHEP")),
                )
                .annotate(
                    TOTAL=ExpressionWrapper(Count("id"), output_field=IntegerField())
                )
                .exclude(Q(localizacao_atual="MOV"))
            )
            return Response(paletes, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        if data["quantidade_paletes"]:
            quantidade_paletes = data.pop("quantidade_paletes")
        else:
            return Response(
                {"quantidade_paletes": ["Este campo é obrigatório."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PaletesControlesSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            for _ in range(0, int(quantidade_paletes)):
                data = {**serializer.validated_data}
                data["localizacao_atual"] = (
                    Filiais.objects.filter(id=data["localizacao_atual"])
                    .values("sigla")
                    .first()["sigla"]
                )
                PaletesControles.objects.create(**data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"success": "Paletes criados com sucesso"},
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request: Request) -> Response:
        data = request.data

        if type(data) is list:
            for item in data:
                palete_id = item.pop("id")

                try:
                    palete = PaletesControles.objects.get(id=palete_id)

                    for key, value in item.items():
                        setattr(palete, key, value)

                    palete.save()
                except PaletesControles.DoesNotExist:
                    return Response(
                        {"error": f"Palete com ID {palete_id} não encontrado"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            return Response(
                {"message": "Objetos atualizados com sucesso"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Lista de dados não fornecida"},
            status=status.HTTP_400_BAD_REQUEST,
        )
