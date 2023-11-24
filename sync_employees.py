import os
import django
import tracemalloc

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_app.settings")
django.setup()

from _service.oracle_db import connect_db, dict_fetchall

from employees.models import Employees
from employees.serializers import EmployeesSerializer


tracemalloc.start()


def sync_employees(cur):
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
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '30' THEN 30
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '31' THEN 31
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '32' THEN 32
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '33' THEN 33
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '34' THEN 34
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '35' THEN 35
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '36' THEN 36
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '37' THEN 37
        WHEN FL.CODIGOEMPRESA = '4' AND FL.CODIGOFL = '1' THEN 41
        WHEN FL.CODIGOEMPRESA = '5' AND FL.CODIGOFL = '1' THEN 151
        WHEN FL.CODIGOEMPRESA = '6' AND FL.CODIGOFL = '1' THEN 161
        WHEN FL.CODIGOEMPRESA = '6' AND FL.CODIGOFL = '2' THEN 162
        WHEN FL.CODIGOEMPRESA = '2' THEN 999
        ElSE 999
    END branch_id,
    FL.NOMEFUNC name,
    TO_CHAR(FL.DTNASCTOFUNC, 'YYYY-MM-DD') date_birth,
    TO_CHAR(FL.DTADMFUNC, 'YYYY-MM-DD') date_admission,
    (SELECT DISTINCT FD.NRDOCTO FROM FLP_DOCUMENTOS FD WHERE FD.CODINTFUNC = FL.CODINTFUNC AND FD.TIPODOCTO = 'RG') rg,
    (SELECT DISTINCT FDD.NRDOCTO FROM FLP_DOCUMENTOS FDD WHERE FDD.CODINTFUNC = FL.CODINTFUNC AND FDD.TIPODOCTO = 'CPF') cpf,
    FL.ENDRUAFUNC street,
    FL.ENDNRFUNC "number",
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

    data = dict_fetchall(cur)

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
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '30' THEN 30
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '31' THEN 31
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '32' THEN 32
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '33' THEN 33
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '34' THEN 34
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '35' THEN 35
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '36' THEN 36
        WHEN FL.CODIGOEMPRESA = '3' AND FL.CODIGOFL = '37' THEN 37
        WHEN FL.CODIGOEMPRESA = '4' AND FL.CODIGOFL = '1' THEN 41
        WHEN FL.CODIGOEMPRESA = '5' AND FL.CODIGOFL = '1' THEN 151
        WHEN FL.CODIGOEMPRESA = '6' AND FL.CODIGOFL = '1' THEN 161
        WHEN FL.CODIGOEMPRESA = '6' AND FL.CODIGOFL = '2' THEN 162
        WHEN FL.CODIGOEMPRESA = '2' THEN 999
        ElSE 999
    END branch_id,
    FL.NOMECOMPLETOPROAUT name,
    TO_CHAR(FL.NASCTOPROAUT, 'YYYY-MM-DD') date_birth,
    TO_CHAR(FL.ADMISSAOPROAUT, 'YYYY-MM-DD') date_admission,
    RGPROAUT rg,
    CPFPROAUT cpf,
    FL.ENDRUAPROAUT street,
    FL.ENDNRPROAUT "number",
    FL.ENDCOMPLPROAUT complement,
    FL.ENDCEPPROAUT cep,
    FL.ENDBAIRROPROAUT district,
    FL.ENDCIDADEPROAUT city,
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
    FL.CONTAPROAUT account,
    CASE
        WHEN FL.SITUACAOPROAUT = 'S' THEN 'ATIVO'
        WHEN FL.SITUACAOPROAUT = 'N' THEN 'DEMITIDO'
    END status
FROM
    FLP_PROAUTONOMOS FL
WHERE
    FL.CODIGOEMPRESA <> '999' AND 
    FL.IDPROAUT = 'E'
"""
    )

    data += dict_fetchall(cur)

    count_create = 0
    count_att = 0
    for employee in data:
        employee["type_contract"] = "CLT"

        if employee["name"]:
            employee["name"] = employee["name"].upper()
        if employee["street"]:
            employee["street"] = employee["street"].upper()
        if employee["complement"]:
            employee["complement"] = employee["complement"].upper()
        if employee["district"]:
            employee["district"] = employee["district"].upper()
        if employee["city"]:
            employee["city"] = employee["city"].upper()

        try:
            emp = Employees.objects.filter(
                name=employee["name"],
                date_admission=employee["date_admission"],
                status=employee["status"],
            ).first()

            serializer = EmployeesSerializer(data=employee, partial=True)
            serializer.is_valid(raise_exception=False)

            for key, value in serializer.validated_data.items():
                setattr(emp, key, value)

            emp.save()
            count_att += 1
        except Exception as e:
            try:
                count_create += 1
                Employees.objects.create(**employee)
            except Exception as e:
                print(e)
                print(employee)


conn = connect_db()
cur = conn.cursor()

sync_employees(cur)

cur.close()
