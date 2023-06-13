from rest_framework.views import APIView, Response, Request, status

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

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
        else:
            paletes = PaletesControles.objects.all().order_by("id")

        serializer = PaletesControlesResponseSerializer(paletes, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        data = request.data

        if type(data) is list:
            objetos = []

            for palete in data:
                autor_id = palete.pop("autor")
                autor = User.objects.get(id=autor_id)

                objeto = PaletesControles(autor=autor, **palete)
                objetos.append(objeto)

            try:
                PaletesControles.objects.bulk_create(objetos)
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {"success": "Paletes criados com sucesso"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": "Lista de dados não fornecida"},
            status=status.HTTP_400_BAD_REQUEST,
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
