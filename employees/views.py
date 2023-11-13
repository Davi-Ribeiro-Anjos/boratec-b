import os

from datetime import datetime
from fpdf import FPDF

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.db.models import Q

from _app import settings
from _service.oracle_db import connect_db, dict_fetchall
from payments_histories.models import PaymentsHistories

from .models import Employees
from .serializers import (
    EmployeesSerializer,
    EmployeesResponseSerializer,
    EmployeesPaymentsResponseSerializer,
)
from .permissions import BasePermission, AdminPermission


class EmployeesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        employees = Employees.objects.filter(**filter).order_by("name")

        serializer = EmployeesResponseSerializer(employees, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = EmployeesSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        employee = Employees.objects.create(**serializer.validated_data)

        serializer = EmployeesResponseSerializer(employee)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class EmployeesDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def patch(self, request: Request, id: int) -> Response:
        employee = get_object_or_404(Employees, id=id)

        serializer = EmployeesSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(employee, key, value)

        employee.save()

        serializer = EmployeesResponseSerializer(employee)

        return Response(serializer.data, status.HTTP_201_CREATED)


class EmployeesPaymentsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def get(self, request: Request) -> Response:
        employees = (
            Employees.objects.filter(type_contract="PJ", status="ATIVO")
            .exclude(branch_id=999)
            .order_by("name")
        )

        serializer = EmployeesPaymentsResponseSerializer(employees, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = EmployeesSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        employee = Employees.objects.create(**serializer.validated_data)

        serializer = EmployeesResponseSerializer(employee)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class EmployeesChoicesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        employees = (
            Employees.objects.filter(status="ATIVO")
            .exclude(branch_id=999)
            .values("id", "name")
            .order_by("name")
        )

        return Response(employees, status.HTTP_200_OK)


class EmployeesDocumentsView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request, id: int) -> Response:
        employee = get_object_or_404(Employees, id=id)

        if employee.type_contract == "CLT":
            data = {
                "NOME": employee.name,
                "RG": employee.rg,
                "CPF": employee.cpf,
                "DATA NASCIMENTO": datetime.strftime(employee.date_birth, "%d/%m/%Y"),
                "EMPRESA": employee.company,
                "TIPO CONTRATO": employee.type_contract,
                "FILIAL": employee.branch.abbreviation,
                "DATA ADMISSÃO": datetime.strftime(employee.date_admission, "%d/%m/%Y"),
                "RUA": employee.street,
                "NUMERO": employee.number,
                "COMPLEMENTO": employee.complement
                if employee.complement
                else "NÃO INFORMADO",
                "CEP": employee.cep,
                "BAIRRO": employee.district,
                "CIDADE": employee.city,
                "UF": employee.uf,
                "BANCO": employee.bank,
                "AGENCIA": employee.agency,
                "CONTA": employee.account,
                "PIX": employee.pix if employee.pix else "NÃO INFORMADO",
            }
        else:
            data = {
                "NOME": employee.name,
                "CNPJ": employee.cnpj,
                "CARGO": employee.role,
                "TIPO CONTRATO": employee.type_contract,
                "EMPRESA": employee.company,
                "FILIAL": employee.branch.abbreviation,
                "DATA ADMISSÃO": datetime.strftime(employee.date_admission, "%d/%m/%Y"),
                "BANCO": employee.bank,
                "AGENCIA": employee.agency,
                "CONTA": employee.account,
                "PIX": employee.pix if employee.pix else "NÃO INFORMADO",
            }

        if employee.epi:
            data["CELULAR"] = "SIM" if employee.epi.phone_model else "NÃO"
            data["NOTEBOOK"] = "SIM" if employee.epi.notebook_model else "NÃO"
        else:
            data["CELULAR"] = "NÃO"
            data["NOTEBOOK"] = "NÃO"

        try:
            pdf = FPDF(orientation="P", unit="mm", format=(210, 297))
            pdf.add_page()
            pdf.ln()

            pdf.image("./_images/logo.png", x=160, y=10, w=35, h=17.5)
            pdf.ln()

            pdf.set_font("Arial", size=20)
            pdf.cell(w=190, h=25, txt="FICHA CADASTRAL", border=0, align="C")
            pdf.ln(30)
            pdf.set_font("Arial", size=12, style="B")

            line_height = pdf.font_size * 2.5
            for k, v in data.items():
                pdf.set_font("Arial", size=12, style="B")
                pdf.cell(70, line_height, k, border=1)  # com barcode = 35 e 65
                pdf.set_font("Arial", size=12)
                pdf.cell(120, line_height, str(v), border=1, ln=1)

            pdf.output(f"FICHA CADASTRAL - {employee.name.upper()}.pdf")

            with open(f"FICHA CADASTRAL - {employee.name.upper()}.pdf", "rb") as f:
                response = HttpResponse(f.read(), content_type="application/pdf")

            f.close()

            os.remove(f"FICHA CADASTRAL - {employee.name.upper()}.pdf")

            response[
                "Content-Disposition"
            ] = f"filename=FICHA CADASTRAL - {employee.name.upper()}.pdf"

            return response

        except Exception as e:
            return Response({"error": e}, status.HTTP_500_INTERNAL_SERVER_ERROR)
