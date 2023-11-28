import os
import csv
import datetime

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from _app import settings
from payments_histories.models import PaymentsHistories

from employees.models import Employees

from .models import PJComplements
from .serializers import (
    PJComplementsSerializer,
    PJComplementsResponseSerializer,
)
from .permissions import AdminPermission


class PJComplementsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = PJComplementsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        pj_complement = PJComplements.objects.create(**serializer.validated_data)

        serializer = PJComplementsResponseSerializer(pj_complement)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PJComplementsDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def patch(self, request: Request, id: int) -> Response:
        pj_complement = get_object_or_404(PJComplements, id=id)

        serializer = PJComplementsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(pj_complement, key, value)

        pj_complement.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PJComplementsEmailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        try:
            if len(data["employees"]) == 0:
                raise ValueError()

            for employee_id in data["employees"]:
                employee = get_object_or_404(Employees, id=employee_id)

                branch = employee.branch
                complement = employee.pj_complements

                total = (
                    complement.salary
                    + complement.allowance
                    + complement.college
                    + complement.covenant_credit
                    + complement.others_credits
                    + complement.housing_allowance
                    - complement.advance_money
                    - complement.covenant_discount
                    - complement.others_discounts
                )

                if data["total"]:
                    title = "NF"
                    text = f"""Favor emitir a NF. de Prestação Serviços

    Período de: {data["period_initial"]} à {data["period_end"]}

    Valor do Serviço: R$ {complement.salary:.2f}
    Premio: R$ {complement.college:.2f}
    Ajuda de custo: R$ {(complement.allowance + complement.housing_allowance):.2f}
    Crédito Convênio: R$ {complement.covenant_credit:.2f}
    Outros Créditos: R$ {complement.others_credits:.2f}

    Adiantamento: R$ {complement.advance_money:.2f}
    Desconto Convênio: R$ {complement.covenant_discount:.2f}
    Outros Descontos: R$ {complement.others_discounts:.2f}

    Total Pagamento: R$ {total:.2f}
    Data de pagamento: {data["date_payment"]}
    Serviço Prestado em: {branch.abbreviation} - {branch.uf}
    Dados Bancários: 
        Banco : {employee.bank}
        Ag    : {employee.agency}
        C.c.  : {employee.account}
    CNPJ: {employee.cnpj}
    PIX: {employee.pix or "Não Informado"}

Favor enviar a NF até {data["date_limit_nf"]}.

Att, Departamento Pessoal
                """
                else:
                    title = "NF ADIANTAMENTO"
                    text = f"""Prestação de Serviços 

    Período de: {data["period_initial"]} à {data["period_end"]}
    Valor do Serviço: R$ {complement.advance_money:.2f}
    Data de pagamento: {data["date_payment"]}
    Serviço Prestado em: {branch.abbreviation} - {branch.uf}
    Dados Bancários: 
        Banco : {employee.bank}
        Ag    : {employee.agency}
        C.c.  : {employee.account}
    CNPJ: {employee.cnpj}
    PIX: {employee.pix or "Não Informado"}

Favor enviar a NF até {data["date_limit_nf"]}.

Att, Departamento Pessoal
                """

                send_mail(
                    subject=title,
                    message=text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[
                        employee.email,
                        "lucas.feitosa@bora.com.br",
                    ],
                    fail_silently=False,
                )

                if data["total"]:
                    payment = {
                        "name": employee.name,
                        "email": employee.email,
                        "cnpj": employee.cnpj,
                        "bank": employee.bank,
                        "agency": employee.agency,
                        "account": employee.account,
                        "operation": employee.operation,
                        "pix": employee.pix,
                        "salary": complement.salary,
                        "allowance": complement.allowance,
                        "college": complement.college,
                        "housing_allowance": complement.housing_allowance,
                        "covenant_credit": complement.covenant_credit,
                        "others_credits": complement.others_credits,
                        "advance_money": complement.advance_money,
                        "covenant_discount": complement.covenant_discount,
                        "others_discounts": complement.others_discounts,
                        "subsistence_allowance": complement.subsistence_allowance,
                        "observation": complement.observation,
                    }

                    PaymentsHistories.objects.create(**payment)

        except KeyError:
            return Response(
                {
                    "message": {
                        "date_limit_nf": "string",
                        "date_payment": "string",
                        "employees": "[int]",
                        "period_end": "string",
                        "period_initial": "string",
                        "total": "bool",
                    }
                },
                status.HTTP_400_BAD_REQUEST,
            )
        except ValueError as e:
            print(e)
            return Response(
                {"message": "Insira algum valor."},
                status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": e}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {},
            status=status.HTTP_204_NO_CONTENT,
        )


class PJComplementsExportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        date = datetime.datetime.strptime(data["date_selected"], "%Y-%m-%d")
        month = date.month
        year = date.year

        payments = PaymentsHistories.objects.filter(
            date_emission__year=year,
            date_emission__month=month,
        )

        with open("Relatório de PJ's.csv", "w", newline="") as csv_file:
            fieldnames = [
                "NOME",
                "EMAIL",
                "CNPJ",
                "BANCO",
                "AGÊNCIA",
                "CONTA",
                "OPERAÇÃO",
                "PIX",
                "SALÁRIO",
                "AJUDA DE CUSTO",
                "FACULDADE",
                "AUXÍLIO MORADIA",
                "CRÉDITO CONVÊNIO",
                "OUTROS CRÉDITOS",
                "ADIANTAMENTO",
                "DESCONTO CONVÊNIO",
                "OUTROS DESCONTOS",
                "TOTAL",
            ]

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

            writer.writeheader()

            for payment in payments:
                total = (
                    payment.salary
                    + payment.allowance
                    + payment.college
                    + payment.covenant_credit
                    + payment.others_credits
                    + payment.housing_allowance
                    - payment.advance_money
                    - payment.covenant_discount
                    - payment.others_discounts
                )
                value = payment.cnpj

                writer.writerow(
                    {
                        "NOME": payment.name,
                        "EMAIL": payment.email,
                        "CNPJ": f"{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}",
                        "BANCO": payment.bank,
                        "AGÊNCIA": payment.agency,
                        "CONTA": payment.account,
                        "OPERAÇÃO": payment.operation,
                        "PIX": payment.pix,
                        "SALÁRIO": payment.salary,
                        "AJUDA DE CUSTO": payment.allowance,
                        "FACULDADE": payment.college,
                        "AUXÍLIO MORADIA": payment.housing_allowance,
                        "CRÉDITO CONVÊNIO": payment.covenant_credit,
                        "OUTROS CRÉDITOS": payment.others_credits,
                        "ADIANTAMENTO": payment.advance_money,
                        "DESCONTO CONVÊNIO": payment.covenant_discount,
                        "OUTROS DESCONTOS": payment.others_discounts,
                        "TOTAL": total,
                    }
                )

        file_csv = FileResponse(
            open("Relatório de PJ's.csv", "rb"),
            content_type="text/csv",
        )
        
        os.remove("Relatório de PJ's.csv")

        return file_csv
