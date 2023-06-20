import os
import ipdb
from fpdf import FPDF
from datetime import datetime


from rest_framework.views import APIView, Response, Request, status

from django.db.models import Q
from django.http import HttpResponse
from django.core.exceptions import FieldError

from filiais.models import Filiais

from .models import Clientes, ClientesFiliais
from .serializers import (
    ClientesSerializer,
    ClientesResponseSerializer,
    ClientesFiliaisSerializer,
)


class ClientesView(APIView):
    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        try:
            clientes_filiais = ClientesFiliais.objects.filter(~Q(saldo=0), **filter)

            serializer = ClientesFiliaisSerializer(clientes_filiais, many=True)

            return Response(serializer.data, status.HTTP_200_OK)
        except FieldError as e:
            return Response({"erro": "Paramêtro não reconhecido"})

    def post(self, request: Request) -> Response:
        try:
            dado = request.data.dict()
        except:
            dado = request.data

        serializer = ClientesSerializer(data=dado)
        serializer.is_valid(raise_exception=True)

        try:
            cliente: Clientes = Clientes.objects.create(**serializer.validated_data)
            filiais = Filiais.objects.all()
            for filial in filiais:
                cliente.filiais.add(filial)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = ClientesResponseSerializer(cliente)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request: Request) -> Response:
        try:
            dado = request.data.dict()
        except:
            dado = request.data

        print(dado)

        try:
            filter = {
                "cliente__id": dado["cliente__id"],
                "filial__id": dado["filial__id"],
                "tipo_palete": dado["tipo_palete"],
            }

            cliente_filial = ClientesFiliais.objects.filter(**filter).first()

            cliente_filial.saldo += int(dado["quantidade_paletes"])
            cliente_filial.save()

            serializer = ClientesFiliaisSerializer(cliente_filial)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class DocumentoView(APIView):
    def get(self, request: Request, id: int) -> Response:
        cliente = ClientesFiliais.objects.filter(id=id).first()

        if cliente.saldo < 0:
            status = "DEVEDOR"
            cliente.saldo *= -1
        else:
            status = "CREDOR"

        data = {
            "Autor": str(request.user).upper(),
            "Razão Social/ Motorista": str(
                cliente.cliente.razao_social_motorista
            ).upper(),
            "Filial": cliente.filial.sigla,
            "Data Solicitação": datetime.now().strftime("%d/%m/%Y %H:%m"),
            "Quantidade": cliente.saldo,
            "Status": status,
        }

        pdf = FPDF(orientation="P", unit="mm", format=(210, 297))
        pdf.add_page()
        pdf.ln()
        pdf.image("_static/images/logo.png", x=160, y=10, w=35, h=17.5)
        pdf.ln()
        pdf.set_font("Arial", size=20)
        pdf.cell(w=190, h=25, txt="Solicitação de Entrega", border=0, align="C")
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
        response["Content-Disposition"] = "filename=some_file.pdf"
        return response


class ClientesChoicesView(APIView):
    def get(self, request: Request) -> Response:
        clientes = Clientes.objects.all().values("id", "razao_social_motorista")

        choices = [
            {"clientes": clientes},
        ]

        return Response(choices, status.HTTP_200_OK)
