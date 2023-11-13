import os
import django
import asyncio
import tracemalloc

from datetime import datetime, date
from asgiref.sync import sync_to_async

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F

from _service.oracle_db import connect_db, dict_fetchall

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_app.settings")
django.setup()

from occurrences.models import Occurrences
from occurrences.serializers import OccurrencesRequestSerializer
from deliveries_histories.models import DeliveriesHistories
from deliveries_histories.serializers import DeliveriesHistoriesRequestSerializer


tracemalloc.start()


async def get_justifications(cur):
    print("JUSTIFICATIVA: INICIANDO QUERY")

    cur.execute(
        f"""
SELECT 
    F1.GARAGEM branch_issuing,
    F1.ID_GARAGEM branch_destination, 
    DECODE(F1.TIPO_DOCTO, 8, 'NFS', 'CTE') document_type,
    F1.CONHECIMENTO cte,
    F1.DATA_EMISSAO date_emission,
    F1.DATA_ENTREGA date_delivery,
    CASE
        WHEN F1.TIPO_DOCTO = 8 THEN TO_CHAR(BC.NFANTASIACLI)
        WHEN F1.TIPO_DOCTO = 57 THEN F1.REM_RZ_SOCIAL
    END sender,
    CASE 
        WHEN F1.TIPO_DOCTO = 8 THEN F11.REC_RZ_SOCIAL
        WHEN F1.TIPO_DOCTO = 57 THEN F1.DEST_RZ_SOCIAL
    END recipient,
    F1.PESO weight,
    CASE
        WHEN F11.DT_PREV_ENTREGA IS NULL THEN '01-01-0001'
        WHEN F11.DT_PREV_ENTREGA IS NOT NULL THEN TO_CHAR(F11.DT_PREV_ENTREGA, 'DD-MM-YYYY') 
    END lead_time,
    CASE 
        WHEN (TRUNC((MIN(F11.DT_PREV_ENTREGA))-(SYSDATE))-1) >= 0 THEN (TRUNC((MIN(F11.DT_PREV_ENTREGA))-(SYSDATE))-1)
        WHEN (TRUNC((MIN(F11.DT_PREV_ENTREGA))-(SYSDATE))*-1) < 0 THEN 0
        WHEN F11.DT_PREV_ENTREGA IS NULL THEN 0
    END opened,
    E2.DESC_LOCALIDADE || '-' || E2.COD_UF delivery_location,
    LISTAGG ((LTRIM (F4.NOTA_FISCAL,0)), ' / ') nf
FROM 
    FTA001 F1,
    FTA011 F11,
    EXA002 E2,
    FTA004 F4,
    BGM_CLIENTE BC               
WHERE
    F1.LOCALID_ENTREGA = E2.COD_LOCALIDADE AND
    F1.CLIENTE_FAT = BC.CODCLI             AND
    
    F1.EMPRESA = F11.EMPRESA               AND
    F1.FILIAL = F11.FILIAL                 AND
    F1.GARAGEM = F11.GARAGEM               AND
    F1.SERIE = F11.SERIE                   AND
    F1.CONHECIMENTO = F11.CONHECIMENTO     AND
    F1.TIPO_DOCTO = F11.TIPO_DOCTO         AND
    
    F1.EMPRESA = F4.EMPRESA                AND
    F1.FILIAL = F4.FILIAL                  AND
    F1.GARAGEM = F4.GARAGEM                AND
    F1.CONHECIMENTO = F4.CONHECIMENTO      AND
    F1.SERIE = F4.SERIE                    AND
    F1.TIPO_DOCTO = F4.TIPO_DOCTO          AND
    
    F1.CARGA_ENCOMENDA IN ('CARGA DIRETA','RODOVIARIO')    AND
    F1.ID_GARAGEM NOT IN (1,23,30)                         AND
    F1.DATA_CANCELADO = '01-JAN-0001'                      AND
    
    F1.EMPRESA = 1                                         AND

    F1.DATA_EMISSAO BETWEEN ((SYSDATE)-2) AND ((SYSDATE)-0)
GROUP BY
    F1.EMPRESA,
    F1.FILIAL,
    F1.GARAGEM,
    F1.ID_GARAGEM,
    F1.TIPO_DOCTO,
    BC.NFANTASIACLI,
    F11.REC_RZ_SOCIAL,
    F1.CONHECIMENTO,
    F1.DATA_EMISSAO,
    F1.DATA_ENTREGA,
    F1.REM_RZ_SOCIAL,
    F1.DEST_RZ_SOCIAL,
    F1.PESO,
    F11.DT_PREV_ENTREGA,
    E2.DESC_LOCALIDADE,
    E2.COD_UF
                    """
    )
    res = dict_fetchall(cur)

    print(f"JUSTIFICATIVA: LEN({len(res)})")

    await insert_to_justification(res)


@sync_to_async
def insert_to_justification(data):
    for justification in data:
        try:
            DeliveriesHistories.objects.get(
                date_emission=justification["date_emission"],
                branch_issuing=justification["branch_issuing"],
                document_type=justification["document_type"],
                cte=justification["cte"],
            )

        except ObjectDoesNotExist:
            lead_time = datetime.strptime(justification["lead_time"], "%d-%m-%Y").date()

            if lead_time == date(1, 1, 1):
                justification["opened"] = 999

            else:
                justification["opened"] = 0

            justification["lead_time"] = lead_time.strftime("%Y-%m-%d")
            justification["date_emission"] = justification["date_emission"].strftime(
                "%Y-%m-%d"
            )
            justification["date_delivery"] = justification["date_delivery"].strftime(
                "%Y-%m-%d"
            )

            if justification["date_delivery"] == "1-01-01":
                justification["date_delivery"] = "0001-01-01"

            if justification["lead_time"] == "1-01-01":
                justification["lead_time"] = "0001-01-01"

            serializer = DeliveriesHistoriesRequestSerializer(data=justification)
            serializer.is_valid()

            DeliveriesHistories.objects.create(**serializer.validated_data)

        except Exception as e:
            print("Error:%s, error_type:%s" % (e, type(e)))


async def get_occurrences(cur):
    print("OCORRENCIAS: INICIANDO QUERY")

    cur.execute(
        f"""
SELECT DISTINCT
    F1.GARAGEM branch_issuing,
    A1.GARAGEM branch,
    A1.NUMERO_CTRC cte,
    DECODE(A1.TIPO_DOCTO, 8, 'NFS', 'CTE') document_type,
    A2.CODIGO occurrence_code,
    A2.DESCRICAO occurrence_description,
    A1.DATA_OCORRENCIA date_emission
FROM 
    ACA001 A1,
    ACA002 A2,
    FTA001 F1
WHERE
    F1.EMPRESA = A1.EMPRESA               AND
    F1.FILIAL = A1.FILIAL                 AND
    F1.GARAGEM = A1.GARAGEM               AND
    F1.SERIE = A1.SERIE_CTRC              AND
    F1.CONHECIMENTO = A1.NUMERO_CTRC      AND
    F1.TIPO_DOCTO = A1.TIPO_DOCTO         AND
    
    A1.COD_OCORRENCIA = A2.CODIGO         AND

    F1.EMPRESA = 1                        AND

    A1.DATA_CADASTRO BETWEEN ((SYSDATE)-2) AND ((SYSDATE)-0)
                    """
    )
    res = dict_fetchall(cur)

    print(f"OCORRENCIAS: LEN({len(res)})")

    await insert_to_occurrences(res)


@sync_to_async
def insert_to_occurrences(data):
    for occurrence in data:
        justification = DeliveriesHistories.objects.filter(
            branch_issuing=occurrence["branch_issuing"], cte=occurrence["cte"]
        ).first()

        del occurrence["branch_issuing"]
        del occurrence["cte"]

        if justification:
            occurrence["justification"] = justification.id

            try:
                Occurrences.objects.get(**occurrence)

            except ObjectDoesNotExist:
                date_delivery = justification.date_delivery
                date_emission = occurrence["date_emission"].date()

                if occurrence["occurrence_description"] == "Entregue":
                    if date_delivery < date_emission:
                        justification.date_delivery = date_emission

                        if justification.opened != 999:
                            if (
                                justification.date_delivery - justification.lead_time
                            ).days <= 0:
                                justification.opened = 0

                            else:
                                justification.opened = (
                                    justification.date_delivery
                                    - justification.lead_time
                                ).days

                justification.save()

                occurrence["date_emission"] = occurrence["date_emission"].strftime(
                    "%Y-%m-%d"
                )

                serializer = OccurrencesRequestSerializer(data=occurrence)
                serializer.is_valid()

                Occurrences.objects.create(**serializer.validated_data)

            except Exception as e:
                print("Error:%s, error_type:%s" % (e, type(e)))


def update_data_not_delivered():
    justifications = DeliveriesHistories.objects.filter(
        ~Q(opened=999), Q(date_delivery=date(1, 1, 1)), confirmed=0
    )

    print(f"ATUALIZANDO {justifications.count()} DADOS SEM ENTREGAS PREENCHIDAS.")

    for just in justifications:
        just.opened = (date.today() - just.lead_time).days

        if just.opened < 0:
            just.opened = 0

        just.save()


def update_data_delivered():
    justifications = DeliveriesHistories.objects.filter(
        ~Q(opened=999), lead_time__lt=F("date_delivery"), confirmed=0
    )

    print(f"ATUALIZANDO {justifications.count()} DADOS COM ENTREGAS PREENCHIDAS.")

    for just in justifications:
        just.opened = (just.date_delivery - just.lead_time).days

        if just.opened >= 999:
            just.opened = 999
        elif just.opened < 0:
            just.opened = 0

        just.save()


conn = connect_db()
cur = conn.cursor()

asyncio.run(get_justifications(cur))
asyncio.run(get_occurrences(cur))

cur.close()

update_data_not_delivered()
update_data_delivered()
