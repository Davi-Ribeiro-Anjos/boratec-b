import os
from fpdf import FPDF
from datetime import datetime
import ipdb


from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db.models import Q
from django.http import HttpResponse
from django.core.exceptions import FieldError

from branches.models import Branches

from .models import Clients, ClientsBranches
from .serializers import (
    ClientsSerializer,
    ClientsResponseSerializer,
    ClientsBranchesSerializer,
)
from .permissions import BasePermission, AdminPermission


class ClientsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        try:
            clients_branches = ClientsBranches.objects.filter(~Q(balance=0), **filter)

            serializer = ClientsBranchesSerializer(clients_branches, many=True)

            return Response(serializer.data, status.HTTP_200_OK)
        except FieldError as e:
            return Response({"erro": "Paramêtro não reconhecido"})

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = ClientsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            client: Clients = Clients.objects.create(**serializer.validated_data)
            branches = Branches.objects.all().exclude(id_garage=99)
            for branch in branches:
                client.branches.add(branch)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = ClientsResponseSerializer(client)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        try:
            filter = {
                "client__id": data["client__id"],
                "branch__id": data["branch__id"],
            }

            client_branch = ClientsBranches.objects.filter(**filter).first()

            client_branch.balance += int(data["quantity_pallets"])
            client_branch.save()

            serializer = ClientsBranchesSerializer(client_branch)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class DocumentView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request, id: int) -> Response:
        client = ClientsBranches.objects.filter(id=id).first()

        if client.balance < 0:
            status = "DEVEDOR"
            client.balance *= -1
        else:
            status = "CREDOR"

        data = {
            # "Autor": str(request.user).upper(),
            "Razão Social/ Motorista": str(client.client.name).upper(),
            "Filial": client.branch.abbreviation,
            "Data Solicitação": datetime.now().strftime("%d/%m/%Y %H:%m"),
            "Quantidade": client.balance,
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


class ClientsChoicesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        clients = Clients.objects.all().values("id", "name")

        return Response(clients, status.HTTP_200_OK)
