import os
import csv
import datetime
from django.http import FileResponse

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from _service.oracle_db import connect_db, dict_fetchall
from _service.limit_size import file_size

from .models import DeliveriesHistories
from .serializers import (
    DeliveriesHistoriesRequestSerializer,
    DeliveriesHistoriesResponseSerializer,
    DeliveriesHistoriesResponseConfirmedSerializer,
    DeliveriesHistoriesPerformancesSerializer,
    DHStatusSerializer,
)
from .permissions import BasePermission, AdminPermission, StatusPermission

import ipdb


class DeliveriesHistoriesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        if "confirmed" in filter:
            if filter["confirmed"] == "false":
                filter["confirmed"] = False
            elif filter["confirmed"] == "true":
                filter["confirmed"] = True

        if "description_justification__isnull" in filter:
            filter["description_justification__isnull"] = True

        deliveries = DeliveriesHistories.objects.filter(**filter).order_by("-opened")

        serializer = DeliveriesHistoriesResponseSerializer(deliveries, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class DeliveriesHistoriesConfirmedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

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


class DeliveriesHistoriesPerformanceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        deliveries = DeliveriesHistories.objects.filter(**filter).order_by(
            "-description_justification", "date_emission", "cte"
        )

        serializer = DeliveriesHistoriesPerformancesSerializer(deliveries, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class DeliveriesHistoriesDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

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


class DeliveriesHistoriesExportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        date = datetime.datetime.strptime(data["date_selected"], "%Y-%m-%d")
        month = date.month
        year = date.year

        filter = {
            "date_emission__year": year,
            "date_emission__month": month,
        }

        try:
            filter["branch_destination"] = data["branch"]
        except:
            pass

        deliveries = DeliveriesHistories.objects.filter(**filter)

        with open(
            "Relatório de Justificativas.csv", "w", newline="", encoding="latin-1"
        ) as csv_file:
            fieldnames = [
                "CTE",
                "DATA DE EMISSAO",
                "LEAD TIME",
                "DATA DE ENTREGA",
                "DESTINATÁRIO",
                "REMETENTE",
                "PESO",
                "NF",
                "TIPO DOCUMENTO",
                "DESCRIÇÃO JUSTIFICATIVA",
                "CIDADE ORIGEM",
                "UF ORIGEM",
                "CIDADE DESTINO",
                "UF DESTINO",
                "STATUS",
            ]

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

            writer.writeheader()

            for delivery in deliveries:
                if delivery.date_delivery and delivery.opened <= 0:
                    status = "NO PRAZO"
                elif delivery.opened == 999:
                    status = "SEM LEADTIME DEFINIDO"
                elif delivery.opened > 0:
                    status = "FORA DO PRAZO"
                elif not delivery.date_delivery:
                    status = "EM ANDAMENTO"

                writer.writerow(
                    {
                        "CTE": delivery.cte,
                        "DATA DE EMISSAO": delivery.date_emission,
                        "LEAD TIME": delivery.lead_time
                        if not str(delivery.lead_time) == "0001-01-01"
                        else None,
                        "DATA DE ENTREGA": delivery.date_delivery
                        if not str(delivery.date_delivery) == "0001-01-01"
                        else None,
                        "DESTINATÁRIO": delivery.recipient,
                        "REMETENTE": delivery.sender,
                        "PESO": delivery.weight,
                        "NF": delivery.nf,
                        "TIPO DOCUMENTO": delivery.document_type,
                        "DESCRIÇÃO JUSTIFICATIVA": delivery.description_justification,
                        "CIDADE ORIGEM": delivery.branch_issuing.name,
                        "UF ORIGEM": delivery.branch_issuing.uf,
                        "CIDADE DESTINO": delivery.branch_destination.name,
                        "UF DESTINO": delivery.branch_destination.uf,
                        "STATUS": status,
                    }
                )

        file_csv = FileResponse(
            open("Relatório de Justificativas.csv", "rb"),
            content_type="text/csv",
        )

        return file_csv


class DeliveriesHistoriesStatusView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, StatusPermission]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        deliveries = DeliveriesHistories.objects.filter(**filter).order_by(
            "recipient", "date_emission"
        )

        serializer = DHStatusSerializer(deliveries, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class DeliveriesHistoriesStatusExportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, StatusPermission]

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        deliveries = DeliveriesHistories.objects.filter(**data).order_by(
            "recipient", "date_emission"
        )

        serializer = DHStatusSerializer(deliveries, many=True)

        data = serializer.data

        with open(
            "Relatório de Status de Entrega.csv", "w", newline="", encoding="latin-1"
        ) as csv_file:
            fieldnames = [
                "CTE",
                "DATA DE EMISSAO",
                "LEAD TIME",
                "DATA DE  ENTREGA",
                "DESTINATÁRIO",
                "REMETENTE",
                "PESO",
                "NF",
                "FILIAL ORIGEM",
                "EMPRESA",
                "CIDADE",
                "UF",
                "FILIAL",
                "STATUS",
                "DATA OCORRÊNCIA",
            ]

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

            writer.writeheader()

            for delivery in data:
                writer.writerow(
                    {
                        "CTE": delivery.get("cte"),
                        "DATA DE EMISSAO": delivery.get("date_emission"),
                        "LEAD TIME": delivery.get("lead_time")
                        if not str(delivery.get("lead_time")) == "0001-01-01"
                        else None,
                        "DATA DE  ENTREGA": delivery.get("date_delivery")
                        if not str(delivery.get("date_delivery")) == "0001-01-01"
                        else None,
                        "DESTINATÁRIO": delivery.get("recipient"),
                        "REMETENTE": delivery.get("sender"),
                        "PESO": delivery.get("weight"),
                        "NF": delivery.get("nf"),
                        "FILIAL ORIGEM": delivery.get("branch_issuing").get(
                            "abbreviation"
                        ),
                        "EMPRESA": delivery.get("branch_destination").get("company"),
                        "CIDADE": delivery.get("branch_destination").get("name"),
                        "UF": delivery.get("branch_destination").get("uf"),
                        "FILIAL": delivery.get("branch_destination").get(
                            "abbreviation"
                        ),
                        "STATUS": delivery.get("last_occurrence").get(
                            "occurrence_description"
                        ),
                        "DATA OCORRÊNCIA": delivery.get("last_occurrence").get(
                            "date_emission"
                        ),
                    }
                )

        file_csv = FileResponse(
            open("Relatório de Status de Entrega.csv", "rb"),
            content_type="text/csv",
        )

        return file_csv


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
