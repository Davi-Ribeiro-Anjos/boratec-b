import os
import ipdb
from datetime import datetime

from fpdf import FPDF
import barcode
from barcode import Code39
from barcode.writer import ImageWriter

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db.models import Count
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


from branches.models import Branches
from pallets_controls.models import PalletsControls

from .models import PalletsMovements
from .serializers import *
from .permissions import BasePermission, AdminPermission


class PalletsMovementsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        params = request.GET.dict()

        list_params = [
            "origin",
            "destiny",
            "vehicle_plate",
            "vehicle_plate__contains",
            "author",
            "author__username",
            "received",
        ]

        wrong_parameters = [param for param in params if not param in list_params]
        if len(wrong_parameters) > 0:
            raise FieldError()

        if "received" in params:
            if params["received"] == "false":
                params["received"] = False
            elif params["received"] == "true":
                params["received"] = True

        try:
            if params:
                movements = PalletsMovements.objects.filter(**params).order_by(
                    "date_request"
                )
                serializer = PalletsMovementsResponseSerializer(movements, many=True)

                return Response(serializer.data, status.HTTP_200_OK)
            else:
                movements = PalletsMovements.objects.all().order_by("date_request")
                serializer = PalletsMovementsResponseSerializer(movements, many=True)

                return Response(serializer.data, status.HTTP_200_OK)
        except FieldError:
            return Response(
                {
                    "mensagem": "Parâmetros incorrretos",
                    "parametros_aceitos": [
                        "numero_request",
                        "date_request",
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
            data_list = request.data.dict()
        except:
            data_list = request.data

        if type(data_list) is list and len(data_list) > 0:
            list_response = []

            for item in data_list:
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                solicitation = (
                    str(time).replace(":", "").replace(" ", "").replace("-", "")
                    + item["vehicle_plate"][5:]
                )

                data = {"request": solicitation, **item}

                serializer = PalletsMovementsSerializer(data=data)
                serializer.is_valid(raise_exception=True)

                branch = Branches.objects.get(id=data["origin"])

                pallets = PalletsControls.objects.filter(
                    current_location=branch.abbreviation, current_movement__isnull=True
                )

                if pallets.count() < int(data["quantity_pallets"]):
                    return Response(
                        {
                            "mensagem": f"A filial {branch.abbreviation} não tem essa quantidade de paletes disponível"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                try:
                    movement: PalletsMovements = PalletsMovements.objects.create(
                        **serializer.validated_data
                    )

                    for _ in range(0, int(data["quantity_pallets"])):
                        pallet = PalletsControls.objects.filter(
                            current_location=branch.abbreviation,
                            current_movement__isnull=True,
                            type_pallet=data["type_pallet"],
                        ).first()

                        item = {
                            "current_movement": movement.request,
                            "current_location": "MOV",
                            "destiny": movement.destiny.abbreviation,
                        }

                        for key, value in item.items():
                            setattr(pallet, key, value)

                        pallet.save()

                    serializer = PalletsMovementsResponseSerializer(movement)

                    list_response.append(serializer.data)

                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            return Response(
                list_response,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": "O json deve ser uma lista preenchida"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PalletsMovementsDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def patch(self, request: Request, id: int) -> Response:
        movement = get_object_or_404(PalletsMovements, id=id)

        serializer = PalletsMovementsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(movement, key, value)

        try:
            pallets = PalletsControls.objects.filter(
                current_movement=movement.request,
                destiny=movement.destiny.abbreviation,
            )

            for pallet in pallets:
                pallet.current_location = pallet.destiny
                pallet.destiny = None
                pallet.current_movement = None

                pallet.save()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        movement.save()

        serializer = PalletsMovementsResponseSerializer(movement)

        return Response(serializer.data, status.HTTP_201_CREATED)


class DocumentView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request, id: int) -> Response:
        movement = PalletsMovements.objects.filter(id=id).first()

        data = {
            "ID Solicitação": movement.request,
            "Origem": movement.origin.abbreviation,
            "Destino": movement.destiny.abbreviation,
            "Placa do Veículo": movement.vehicle_plate.upper(),
            "Data Solicitação": datetime.strftime(
                movement.date_request, "%d/%m/%Y %H:%m"
            ),
            "Quantidade": movement.quantity_pallets,
            "Autor": movement.author.name.upper(),
            "Motorista": movement.driver,
            "Conferente": movement.checker,
        }

        # Gerar código de barras
        pdf = FPDF(orientation="P", unit="mm", format=(210, 297))
        pdf.add_page()
        pdf.ln()

        EAN = barcode.get_barcode_class("ean13")
        my_ean = EAN(data["ID Solicitação"], writer=ImageWriter())
        my_ean.save("barcode")

        pdf.image(
            "./barcode.png", x=48, y=150, w=120, h=30
        )  # Posição(x, y) Tamanho(w, h)
        pdf.image("./_images/logo.png", x=160, y=10, w=35, h=17.5)
        pdf.ln()
        pdf.set_font("Arial", size=20)
        pdf.cell(w=190, h=25, txt="Solicitação de Transferência", border=0, align="C")
        pdf.ln(30)
        pdf.set_font("Arial", size=12, style="B")

        line_height = pdf.font_size * 2.5
        for k, v in data.items():
            pdf.set_font("Arial", size=12, style="B")
            pdf.cell(60, line_height, k, border=1)  # com barcode = 35 e 65
            pdf.set_font("Arial", size=12)
            pdf.cell(130, line_height, str(v), border=1, ln=1)
        pdf.output("GFG.pdf")
        with open("GFG.pdf", "rb") as f:
            response = HttpResponse(f.read(), content_type="application/pdf")
        f.close()
        os.remove("GFG.pdf")
        os.remove("barcode.png")
        response["Content-Disposition"] = "filename=some_file.pdf"
        return response
