from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from _service.oracle_db import connect_db, dict_fetchall

from pj_complements.models import PJComplements

from .models import Employees
from .serializers import EmployeesSerializer, EmployeesResponseSerializer

import ipdb


class EmployeesView(APIView):
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

        # data["pj_complements"] = PJComplements.objects.filter(
        #     id=data["pj_complements"]
        # ).first()

        serializer = EmployeesSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        employee = Employees.objects.create(**serializer.validated_data)

        serializer = EmployeesResponseSerializer(employee)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class EmployeesDetailView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        employee = get_object_or_404(Employees, id=id)
        serializer = EmployeesSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(employee, key, value)

        employee.save()

        serializer = EmployeesResponseSerializer(employee)

        return Response(serializer.data, status.HTTP_201_CREATED)


class EmployeesChoicesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        employees = Employees.objects.filter(status="ATIVO").values("id", "name")

        return Response(employees, status.HTTP_200_OK)


class EmployeesOracleView(APIView):
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
                employee["type_contract"] = "CLT"
                Employees.objects.create(**employee)

        return Response(
            {"message": f"{count_create} funcionários foram adicionados"},
            status.HTTP_200_OK,
        )
