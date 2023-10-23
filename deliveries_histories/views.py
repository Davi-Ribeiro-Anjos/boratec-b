import os
import asyncio
import ipdb

from datetime import datetime, date
from fpdf import FPDF
from asgiref.sync import sync_to_async

from rest_framework import serializers
from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q, F

from _service.oracle_db import connect_db, dict_fetchall
from _service.limit_size import file_size

from branches.models import Branches
from occurrences.models import Occurrences

from .models import DeliveriesHistories
from .serializers import (
    DeliveriesHistoriesRequestSerializer,
    DeliveriesHistoriesResponseSerializer,
    DeliveriesHistoriesResponseConfirmedSerializer,
)


class DeliveriesHistoriesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        if "confirmed" in filter:
            if filter["confirmed"] == "false":
                filter["confirmed"] = False
            elif filter["confirmed"] == "true":
                filter["confirmed"] = True

        if "description_justification__isnull" in filter:
            filter["description_justification__isnull"] = True

        deliveries = DeliveriesHistories.objects.filter(**filter).order_by(
            "date_emission", "cte"
        )

        serializer = DeliveriesHistoriesResponseSerializer(deliveries, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class DeliveriesHistoriesConfirmedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        filter = {
            "confirmed": False,
            "description_justification__isnull": False,
            "file__isnull": False,
        }

        deliveries = DeliveriesHistories.objects.filter(**filter).order_by(
            "date_emission", "cte"
        )

        serializer = DeliveriesHistoriesResponseConfirmedSerializer(
            deliveries, many=True
        )

        return Response(serializer.data, status.HTTP_200_OK)


class DeliveriesHistoriesDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, id: int) -> Response:
        file = request.FILES.get("file")

        try:
            file_size(file, 5)
        except ValidationError as e:
            return Response({"message": e.args[0]}, status.HTTP_400_BAD_REQUEST)

        justification = get_object_or_404(DeliveriesHistories, id=id)

        serializer = DeliveriesHistoriesRequestSerializer(
            data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(justification, key, value)

        justification.save()

        serializer = DeliveriesHistoriesResponseSerializer(justification)

        return Response(serializer.data, status.HTTP_200_OK)


class DeliveriesHistoriesQueriesNFView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, nf: str) -> Response:
        if nf:
            while len(nf) < 10:
                nf = "0" + nf

            conn = connect_db()
            cur = conn.cursor()
            cur.execute(
                f"""
SELECT
    F1.GARAGEM garage,
    F1.CONHECIMENTO knowledge,
    TO_CHAR(F1.DATA_EMISSAO, 'DD/MM/YYYY') date_emission,
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
        WHEN F11.DT_PREV_ENTREGA IS NOT NULL THEN TO_CHAR(F11.DT_PREV_ENTREGA, 'DD/MM/YYYY')
    END date_forecast,
    E2.DESC_LOCALIDADE || '-' || E2.COD_UF delivery_location,
    F1.CARGA_ENCOMENDA order_loading,
    (LTRIM (F4.NOTA_FISCAL,0)) nf
FROM 
    FTA001 F1,
    FTA011 F11,
    EXA002 E2,
    FTA004 F4,
    BGM_CLIENTE BC               
WHERE
    F1.LOCALID_ENTREGA = E2.COD_LOCALIDADE   AND
    F1.CLIENTE_FAT = BC.CODCLI               AND
    
    F1.EMPRESA = F11.EMPRESA                 AND
    F1.FILIAL = F11.FILIAL                   AND
    F1.GARAGEM = F11.GARAGEM                 AND
    F1.SERIE = F11.SERIE                     AND
    F1.CONHECIMENTO = F11.CONHECIMENTO       AND
    F1.TIPO_DOCTO = F11.TIPO_DOCTO           AND
    
    F1.EMPRESA = F4.EMPRESA                  AND
    F1.FILIAL = F4.FILIAL                    AND
    F1.GARAGEM = F4.GARAGEM                  AND
    F1.CONHECIMENTO = F4.CONHECIMENTO        AND
    F1.SERIE = F4.SERIE                      AND
    F1.TIPO_DOCTO = F4.TIPO_DOCTO            AND
    
    F1.DATA_CANCELADO = '01-JAN-0001'        AND

    F4.NOTA_FISCAL = '{nf}'
GROUP BY
    F1.EMPRESA,
    F1.FILIAL,
    F1.GARAGEM,
    F1.ID_GARAGEM,
    F1.TIPO_DOCTO,
    F1.CARGA_ENCOMENDA,
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
    E2.COD_UF,
    F4.NOTA_FISCAL
ORDER BY
    F1.DATA_EMISSAO DESC
                    """
            )

            justifications = dict_fetchall(cur)

            cur.execute(
                f"""
SELECT 
    E6.COD_MANIFESTO packing_list,
    DECODE(E5.ENTREGA_TRANSF,'T','TRANSFERENCIA','ENTREGA') delivery_type,
    VE.PREFIXOVEIC plate,
    TO_CHAR(E5.DATA_SAIDA, 'DD/MM/YYYY') date_exit,
    MO.NOME driver,
    MO.TELEFONE phone,
    E5.GARAGEM garage,
    E6.NUMERO_CTRC knowledge,
    CASE
        WHEN VE.CODIGOTPVEIC = 1 THEN 'VAN - PASSAGEIROS'
        WHEN VE.CODIGOTPVEIC = 2 THEN 'CAMINHAO'
        WHEN VE.CODIGOTPVEIC = 3 THEN 'CAVALO'
        WHEN VE.CODIGOTPVEIC = 4 THEN 'CARRETA'
        WHEN VE.CODIGOTPVEIC = 5 THEN 'VUC - MINI CAMINHAO'
        WHEN VE.CODIGOTPVEIC = 6 THEN 'BI TRUCK'
        WHEN VE.CODIGOTPVEIC = 7 THEN 'TOCO'
        WHEN VE.CODIGOTPVEIC = 8 THEN '3/4'
        WHEN VE.CODIGOTPVEIC = 9 THEN 'TRUCK'
        WHEN VE.CODIGOTPVEIC = 10 THEN 'VEICULO APOIO'
        WHEN VE.CODIGOTPVEIC = 11 THEN 'PASSAGEIRO'
        WHEN VE.CODIGOTPVEIC = 12 THEN 'PASSAGEIRO AUTOMOVEL'
        WHEN VE.CODIGOTPVEIC = 13 THEN 'VW/24.280 CRM 6X2'
        WHEN VE.CODIGOTPVEIC = 14 THEN 'FIORINO'
        WHEN VE.CODIGOTPVEIC = 15 THEN 'HR'
    END type_vehicle,
    (LTRIM (F4.NOTA_FISCAL,0)) nf
FROM 
    FTA001 F1,
    FTA004 F4,
    EXA026 E6,
    EXA025 E5,
    FRT_CADVEICULOS VE,
    VWCGS_FUNCIONARIOSCOMAGREGADO MO
WHERE
    F1.EMPRESA = E6.EMPRESA                AND
    F1.FILIAL = E6.FILIAL                  AND
    F1.GARAGEM = E6.GARAGEM                AND
    F1.SERIE = E6.SERIE_CTRC               AND
    F1.CONHECIMENTO = E6.NUMERO_CTRC       AND
   
    E5.RECNUM = E6.RECNUM_EXA025           AND
    
    E5.ID_MOTORISTA = MO.IDENTIFICACAO(+)  AND
    E5.MOTORISTA = MO.CODINTFUNC (+)       AND
    E5.VEICULO = VE.CODIGOVEIC (+)         AND
    
    F1.EMPRESA = F4.EMPRESA                AND
    F1.FILIAL = F4.FILIAL                  AND
    F1.GARAGEM = F4.GARAGEM                AND
    F1.CONHECIMENTO = F4.CONHECIMENTO      AND
    F1.SERIE = F4.SERIE                    AND
    F1.TIPO_DOCTO = F4.TIPO_DOCTO          AND
    
    F1.DATA_CANCELADO = '01-JAN-0001'      AND

    F4.NOTA_FISCAL = '{nf}'
                    """
            )

            packing_list = dict_fetchall(cur)

            justifications_list = []
            for just in justifications:
                if (
                    just["order_loading"] == "CARGA DIRETA"
                    or just["order_loading"] == "RODOVIARIO"
                ):
                    cur.execute(
                        f"""
SELECT DISTINCT
    A1.DATA_OCORRENCIA date_occurrence,
    A2.DESCRICAO description_occurrence
FROM
    ACA001 A1,
    ACA002 A2
WHERE
    A1.COD_OCORRENCIA = A2.CODIGO          AND
    A1.NUMERO_CTRC = {just['knowledge']}   AND
    A1.GARAGEM = {just['garage']}
ORDER BY 
	A1.DATA_OCORRENCIA
                    """
                    )
                    just["occurrences"] = dict_fetchall(cur)

                    for occu in just["occurrences"]:
                        occu["date_occurrence"] = occu["date_occurrence"].strftime(
                            "%d/%m/%Y"
                        )

                    just["packing_list"] = [
                        pack
                        for pack in packing_list
                        if just["knowledge"] == pack["knowledge"]
                    ]

                    justifications_list.append(just)

            cur.close()

        return Response(justifications_list, status.HTTP_200_OK)


class DeliveriesHistoriesSyncView(APIView):
    def post(self, request: Request) -> Response:
        conn = connect_db()
        cur = conn.cursor()

        print("ok")
        asyncio.run(get_justificifcatives(cur))
        # asyncio.run(get_occurrences(cur))

        cur.close()

        update_data_not_delivered()
        update_data_delivered()

        return Response({}, status.HTTP_204_NO_CONTENT)


async def get_justificifcatives(cur):
    print("JUSTIFICATIVA: INICIANDO QUERY")

    cur.execute(
        f"""
SELECT 
    F1.GARAGEM garage,
    F1.ID_GARAGEM id_garage, 
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
        WHEN F1.DATA_ENTREGA = '01-JAN-0001' THEN 'NAO ENTREGUE'
        WHEN F1.DATA_ENTREGA <> '01-JAN-0001' THEN CASE
            WHEN (F1.DATA_ENTREGA - F11.DT_PREV_ENTREGA) < 0 THEN 'ADIANTADO'
            WHEN (F1.DATA_ENTREGA - F11.DT_PREV_ENTREGA) > 0 THEN 'ATRASADO'
            END
    END LEADTIME,
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

    F1.DATA_EMISSAO BETWEEN ((SYSDATE)-85) AND ((SYSDATE)-41)
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

    await insert_to_justificative(res)


@sync_to_async
def insert_to_justificative(data):
    for justificative in data:
        try:
            DeliveriesHistories.objects.get(
                garage=justificative["garage"],
                document_type=justificative["document_type"],
                cte=justificative["cte"],
            )

        except ObjectDoesNotExist:
            del justificative["leadtime"]

            lead_time = datetime.strptime(justificative["lead_time"], "%d-%m-%Y").date()

            if lead_time == date(1, 1, 1):
                justificative["opened"] = 999

            else:
                justificative["opened"] = 0

            try:
                branch = Branches.objects.get(id_garage=justificative["id_garage"])
                justificative["branch"] = branch

            except:
                pass

            justificative["lead_time"] = lead_time

            DeliveriesHistories.objects.create(**justificative)

        except Exception as e:
            print("Error:%s, error_type:%s" % (e, type(e)))


async def get_occurrences(cur):
    print("OCORRENCIAS: INICIANDO QUERY")

    cur.execute(
        f"""
SELECT DISTINCT
    A1.GARAGEM garage,
    A1.NUMERO_CTRC cte,
    A1.TIPO_DOCTO document_type,
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
    F1.SERIE = A1.SERIE_CTRC                AND
    F1.CONHECIMENTO = A1.NUMERO_CTRC     AND
    F1.TIPO_DOCTO = A1.TIPO_DOCTO         AND
    
    A1.COD_OCORRENCIA = A2.CODIGO AND
    A1.DATA_CADASTRO BETWEEN ((SYSDATE)-40) AND ((SYSDATE)-20) AND
    F1.ID_GARAGEM = 6
                    """
    )
    res = dict_fetchall(cur)

    print(f"OCORRENCIAS: LEN({len(res)})")

    await insert_to_occurences(res)


@sync_to_async
def insert_to_occurences(data):
    for occurrence in data:
        justificative = DeliveriesHistories.objects.filter(
            garage=occurrence["garage"], cte=occurrence["cte"]
        ).first()

        if justificative:
            occurrence["justification"] = justificative

            try:
                Occurrences.objects.get(**occurrence)

            except ObjectDoesNotExist:
                date_delivery_inicial = justificative.date_delivery
                date_emission = occurrence["date_emission"].date()

                if occurrence["occurrence_description"] == "Entregue":
                    if date_delivery_inicial < date_emission:
                        justificative.date_delivery = date_emission

                        if justificative.opened != 999:
                            if (
                                justificative.date_delivery - justificative.lead_time
                            ).days <= 0:
                                justificative.opened = 0

                            else:
                                justificative.opened = (
                                    justificative.date_delivery
                                    - justificative.lead_time
                                ).days

                justificative.save()

                try:
                    occurrence["branch"] = justificative.branch

                except:
                    pass

                Occurrences.objects.create(**occurrence)

            except Exception as e:
                print("Error:%s, error_type:%s" % (e, type(e)))


def update_data_not_delivered():
    justificatives = DeliveriesHistories.objects.filter(
        ~Q(opened=999), Q(date_delivery=date(1, 1, 1)), confirmed=0
    )
    print(f"ATUALIZANDO {justificatives.count()} DADOS SEM ENTREGAS PREENCHIDAS.")
    for just in justificatives:
        just.opened = (date.today() - just.lead_time).days

        if just.opened < 0:
            just.opened = 0

        just.save()


def update_data_delivered():
    justificatives = DeliveriesHistories.objects.filter(
        lead_time__lt=F("date_delivery"), confirmed=0
    )
    print(f"ATUALIZANDO {justificatives.count()} DADOS COM ENTREGAS PREENCHIDAS.")

    for just in justificatives:
        just.opened = (just.date_delivery - just.lead_time).days

        if just.opened > 999:
            just.opened = 999

        just.save()
