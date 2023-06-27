import os
import ipdb
from datetime import datetime

from fpdf import FPDF
import barcode
from barcode import Code39
from barcode.writer import ImageWriter

from rest_framework.views import APIView, Response, Request, status

from django.db.models import Count
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


from filiais.models import Filiais
from paletes_controles.models import PaletesControles

from .models import PaletesMovimentos
from .serializers import *


class PaletesMovimentosView(APIView):
    def get(self, request: Request) -> Response:
        params = request.GET.dict()

        lista_params = [
            "origem",
            "destino",
            "placa_veiculo",
            "placa_veiculo__contains",
            "autor",
            "autor__username",
            "recebido",
        ]

        params_errados = [param for param in params if not param in lista_params]
        if len(params_errados) > 0:
            raise FieldError()

        if "recebido" in params:
            if params["recebido"] == "false":
                params["recebido"] = False
            elif params["recebido"] == "true":
                params["recebido"] = True

        try:
            if params:
                movimentos = PaletesMovimentos.objects.filter(**params).order_by(
                    "data_solicitacao"
                )
                serializer = PaletesMovimentosResponseSerializer(movimentos, many=True)

                return Response(serializer.data, status.HTTP_200_OK)
            else:
                movimentos = PaletesMovimentos.objects.all().order_by(
                    "data_solicitacao"
                )
                serializer = PaletesMovimentosResponseSerializer(movimentos, many=True)

                return Response(serializer.data, status.HTTP_200_OK)
        except FieldError:
            return Response(
                {
                    "mensagem": "Parâmetros incorrretos",
                    "parametros_aceitos": [
                        "numero_solicitacao",
                        "data_solicitacao_bo",
                        "status",
                        "solicitante",
                        "filial",
                    ],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": e}, status.HTTP_400_BAD_REQUEST)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        tempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        solicitacao = (
            str(tempo).replace(":", "").replace(" ", "").replace("-", "")
            + data["placa_veiculo"][5:]
        )

        data = {"solicitacao": solicitacao, **data}

        serializer = PaletesMovimentosSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        filial = Filiais.objects.get(id=data["origem"])

        paletes = PaletesControles.objects.filter(
            localizacao_atual=filial.sigla, movimento_atual__isnull=True
        )

        if paletes.count() < int(data["quantidade_paletes"]):
            return Response(
                {
                    "mensagem": f"A filial {filial.sigla} não tem essa quantidade de paletes disponível"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            movimento: PaletesMovimentos = PaletesMovimentos.objects.create(
                **serializer.validated_data
            )

            for _ in range(0, int(data["quantidade_paletes"])):
                palete = PaletesControles.objects.filter(
                    localizacao_atual=filial.sigla,
                    movimento_atual__isnull=True,
                    tipo_palete=data["tipo_palete"],
                ).first()

                item = {
                    "movimento_atual": movimento.solicitacao,
                    "localizacao_atual": "MOV",
                    "destino": movimento.destino.sigla,
                }

                for key, value in item.items():
                    setattr(palete, key, value)

                palete.save()

            serializer: PaletesMovimentosResponseSerializer = (
                PaletesMovimentosResponseSerializer(movimento)
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaletesMovimentosDetailView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        solicitacao = get_object_or_404(PaletesMovimentos, id=id)
        serializer = PaletesMovimentosSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(solicitacao, key, value)

        try:
            paletes = PaletesControles.objects.filter(
                movimento_atual=solicitacao.solicitacao,
                destino=solicitacao.destino.sigla,
            )

            for palete in paletes:
                palete.localizacao_atual = palete.destino
                palete.destino = None
                palete.movimento_atual = None

                palete.save()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        solicitacao.save()

        serializer = PaletesMovimentosResponseSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_201_CREATED)


class DocumentoView(APIView):
    def get(self, request: Request, id: int) -> Response:
        movimento = PaletesMovimentos.objects.filter(id=id).first()

        data = {
            "ID Solicitação": movimento.solicitacao,
            "Origem": movimento.origem.sigla,
            "Destino": movimento.destino.sigla,
            "Placa do Veículo": movimento.placa_veiculo.upper(),
            "Data Solicitação": datetime.strftime(
                movimento.data_solicitacao, "%d/%m/%Y %H:%m"
            ),
            "Quantidade": movimento.quantidade_paletes,
            "Autor": movimento.autor.username.upper(),
            "Motorista": movimento.motorista,
            "Conferente": movimento.conferente,
        }

        # Gerar código de barras
        pdf = FPDF(orientation="P", unit="mm", format=(210, 297))
        pdf.add_page()
        pdf.ln()

        EAN = barcode.get_barcode_class("ean13")
        my_ean = EAN(data["ID Solicitação"], writer=ImageWriter())
        my_ean.save("barcode")

        pdf.image(
            "./barcode.png", x=48, y=150, w=120, h=30
        )  # Posição(x, y) Tamanho(w, h)
        pdf.image("_static/images/logo.png", x=160, y=10, w=35, h=17.5)
        pdf.ln()
        pdf.set_font("Arial", size=20)
        pdf.cell(w=190, h=25, txt="Solicitação de Transferência", border=0, align="C")
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
        os.remove("barcode.png")
        response["Content-Disposition"] = "filename=some_file.pdf"
        return response
