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
