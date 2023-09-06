import os
from datetime import datetime
from fpdf import FPDF

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail

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
        employees = Employees.objects.filter(type_contract="PJ").order_by("name")

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


class EmployeesPaymentsEmailView(APIView):
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

    Observação: {complement.observation}

Favor enviar a NF até {data["date_limit_nf"]}.

Att,
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

    Observação: {complement.observation}

Favor enviar a NF até {data["date_limit_nf"]}.

Att,
                """

                send_mail(
                    subject=title,
                    message=text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[
                        employee.user.email,
                        "lucas.feitosa@bora.com.br",
                    ],
                    fail_silently=False,
                )

                payment = {
                    "name": employee.name,
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
                    "data_emission": complement.data_emission,
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
        except ValueError:
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


# class EmployeesPaymentsXlsxView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request: Request) -> Response:
#         try:
#             data = request.data.dict()
#         except:
#             data = request.data

#         serializer = EmployeesSerializer(data=data)
#         serializer.is_valid(raise_exception=True)

#         employee = Employees.objects.create(**serializer.validated_data)

#         serializer = EmployeesResponseSerializer(employee)

#         return Response(
#             serializer.data,
#             status=status.HTTP_201_CREATED,
#         )


class EmployeesChoicesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        employees = (
            Employees.objects.filter(status="ATIVO")
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

            pdf.image("_static/images/logo.png", x=160, y=10, w=35, h=17.5)
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


class EmployeesOracleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request: Request) -> Response:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
SELECT DISTINCT
    CASE
        WHEN FL.CODIGOEMPRESA = 1 THEN 'BORA'
        WHEN FL.CODIGOEMPRESA = 2 THEN 'TRANSERVO'
        WHEN FL.CODIGOEMPRESA = 3 THEN 'BORBON'
        WHEN FL.CODIGOEMPRESA = 4 THEN 'TRANSFOOD'
        WHEN FL.CODIGOEMPRESA = 5 THEN 'JSR'
        WHEN FL.CODIGOEMPRESA = 6 THEN 'JC'
    END company,
    CASE
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '1'  THEN 1
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '2'  THEN 2
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '3'  THEN 3
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '4'  THEN 4
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '5'  THEN 5
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '6'  THEN 6
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '7'  THEN 7
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '8'  THEN 8
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '9'  THEN 9
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '10' THEN 10
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '11' THEN 11
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '12' THEN 12
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '13' THEN 13
        WHEN FL.CODIGOEMPRESA = '1' AND FL.CODIGOFL = '14' THEN 14
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '30' THEN 15
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '31' THEN 16
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '32' THEN 17
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '33' THEN 18
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '34' THEN 19
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '35' THEN 20
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '36' THEN 21
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '37' THEN 22
        WHEN FL.CODIGOEMPRESA = '4' AND FL.CODIGOFL = '1' THEN 23
        WHEN FL.CODIGOEMPRESA = '5' AND FL.CODIGOFL = '1' THEN 24
        WHEN FL.CODIGOEMPRESA = '6' AND FL.CODIGOFL = '1' THEN 25
        WHEN FL.CODIGOEMPRESA = '2' THEN 99
    END branch_id,
    FL.NOMEFUNC name,
    TO_CHAR(FL.DTNASCTOFUNC, 'YYYY-MM-DD') date_birth,
    TO_CHAR(FL.DTADMFUNC, 'YYYY-MM-DD') date_admission,
    (SELECT DISTINCT FD.NRDOCTO FROM FLP_DOCUMENTOS FD WHERE FD.CODINTFUNC = FL.CODINTFUNC AND FD.TIPODOCTO = 'RG') rg,
    (SELECT DISTINCT FDD.NRDOCTO FROM FLP_DOCUMENTOS FDD WHERE FDD.CODINTFUNC = FL.CODINTFUNC AND FDD.TIPODOCTO = 'CPF') cpf,
    FL.ENDRUAFUNC street,
    FL.ENDNRFUNC num,
    FL.ENDCOMPLFUNC complement,
    FL.ENDCEPFUNC cep,
    FL.ENDBAIRROFUNC district,
    FL.ENDCIDADEFUNC city,
    FL.CODIGOUF uf,
    CASE 
        WHEN FL.CODBANCO = 341 THEN 'ITAÚ'
        WHEN FL.CODBANCO = 237 THEN 'BRADESCO'
        WHEN FL.CODBANCO = 33 THEN 'SANTANDER'
        WHEN FL.CODBANCO = 104 THEN 'CAIXA'
        WHEN FL.CODBANCO = 260 THEN 'NUBANK'
        WHEN FL.CODBANCO = 77 THEN 'INTERMEDIUM'
        WHEN FL.CODBANCO = 337 THEN 'MS SOCIEDADE'
        WHEN FL.CODBANCO = 665 THEN 'VANTORANTIM'
        WHEN FL.CODBANCO = 100 THEN 'PLANNER CORRETORA'
        WHEN FL.CODBANCO = 1 THEN 'BANCO DO BRASIL'
    END bank,
    FL.CODAGENCIA agency,
    FL.CONTACORFUNC account,
    CASE
        WHEN FL.SITUACAOFUNC = 'A' THEN 'ATIVO'
        WHEN FL.SITUACAOFUNC = 'D' THEN 'DEMITIDO'
        WHEN FL.SITUACAOFUNC = 'F' THEN 'AFASTADO'
    END status
FROM
    FLP_FUNCIONARIOS FL
WHERE
    FL.CODIGOEMPRESA <> '999'
            """
        )

        data: list[Employees] = dict_fetchall(cur)
        cur.close()

        count_create = 0
        for employee in data:
            employee["type_contract"] = "CLT"
            employee["number"] = employee["num"]

            del employee["num"]

            try:
                emp = Employees.objects.get(
                    name=employee["name"],
                    date_admission=employee["date_admission"],
                    status=employee["status"],
                )

                serializer = EmployeesSerializer(data=employee, partial=True)
                serializer.is_valid(raise_exception=False)

                for key, value in serializer.validated_data.items():
                    setattr(emp, key, value)

                emp.save()
            except Exception:
                count_create += 1
                Employees.objects.create(**employee)

        return Response(
            {"message": f"{count_create} employeeionários foram adicionados"},
            status.HTTP_200_OK,
        )
