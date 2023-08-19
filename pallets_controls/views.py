from rest_framework.views import APIView, Response, Request, status

from django.contrib.auth.models import User
from django.db.models import Count, Q, ExpressionWrapper, IntegerField
from django.shortcuts import get_object_or_404

from branches.models import Branches

from .models import PalletsControls
from .serializers import *


class PalletsControlsView(APIView):
    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        if filter:
            try:
                pallets = PalletsControls.objects.filter(**filter).order_by("id")
            except Exception:
                pallets = PalletsControls.objects.all().order_by("id")

            serializer = PalletsControlsResponseSerializer(pallets, many=True)

            return Response(serializer.data, status.HTTP_200_OK)
        else:
            pallets = (
                PalletsControls.objects.all()
                .values("current_location")
                .annotate(
                    PBR=Count("id", filter=Q(type_pallet="PBR")),
                    CHEP=Count("id", filter=Q(type_pallet="CHEP")),
                )
                .annotate(
                    TOTAL=ExpressionWrapper(Count("id"), output_field=IntegerField())
                )
                .exclude(Q(current_location="MOV"))
            )
            return Response(pallets, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        if data["quantity_pallets"]:
            quantity_pallets = data.pop("quantity_pallets")
        else:
            return Response(
                {"quantity_pallets": ["Este campo é obrigatório."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PalletsControlsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            for _ in range(0, int(quantity_pallets)):
                data = {**serializer.validated_data}
                data["current_location"] = (
                    Branches.objects.filter(id=data["current_location"])
                    .values("abbreviation")
                    .first()["abbreviation"]
                )
                PalletsControls.objects.create(**data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        pallets = (
            PalletsControls.objects.filter(current_location=data["current_location"])
            .values("current_location")
            .annotate(
                PBR=Count("id", filter=Q(type_pallet="PBR")),
                CHEP=Count("id", filter=Q(type_pallet="CHEP")),
            )
            .annotate(TOTAL=ExpressionWrapper(Count("id"), output_field=IntegerField()))
            .exclude(Q(current_location="MOV"))
        )

        return Response(
            pallets[0],
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request: Request) -> Response:
        data = request.data

        if type(data) is list:
            for item in data:
                pallet_id = item.pop("id")

                try:
                    pallet = PalletsControls.objects.get(id=pallet_id)

                    for key, value in item.items():
                        setattr(pallet, key, value)

                    pallet.save()
                except PalletsControls.DoesNotExist:
                    return Response(
                        {"error": f"Palete com ID {pallet_id} não encontrado"},
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
