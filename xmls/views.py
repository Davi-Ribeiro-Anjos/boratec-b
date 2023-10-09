import io
import os
import re
import email
import datetime
import poplib
import warnings
import numpy as np
import pandas as pd
import ipdb

from io import BytesIO
from zipfile import ZipFile
from xml.dom import minidom

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.utils import dateformat
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import F

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from _app import settings

from skus.models import Skus
from branches.models import Branches

from .models import Xmls
from .serializers import (
    XmlsResponseSerializer,
)
from .permissions import BasePermission

warnings.simplefilter(action="ignore", category=FutureWarning)


def getText(nodelist):
    document = nodelist.getElementsByTagName("det")
    rc = []
    emit = (
        nodelist.getElementsByTagName("emit")[0]
        .getElementsByTagName("CNPJ")[0]
        .firstChild.nodeValue
    )
    for q in document:
        var1 = q.getElementsByTagName("prod")[0]
        sku = var1.getElementsByTagName("cProd")[0].firstChild.nodeValue
        descprod = var1.getElementsByTagName("xProd")[0].firstChild.nodeValue
        un = var1.getElementsByTagName("uTrib")[0].firstChild.nodeValue
        qnt = var1.getElementsByTagName("qTrib")[0].firstChild.nodeValue.split(".")[0]
        if emit == "00763832000160":
            un2 = "CX"
            qnt2 = (
                q.getElementsByTagName("infAdProd")[0]
                .firstChild.nodeValue[19:]
                .split(" ")[0]
            )
        else:
            un2 = var1.getElementsByTagName("uCom")[0].firstChild.nodeValue
            qnt2 = var1.getElementsByTagName("qCom")[0].firstChild.nodeValue.split(".")[
                0
            ]
        all = {
            "sku": sku,
            "descprod": descprod,
            "un": un,
            "qnt": qnt,
            "un2": un2,
            "qnt2": qnt2,
        }
        rc.append(all)
    return rc


def getFiles(*args):
    s = BytesIO()

    zf = ZipFile(s, "w")
    for q in args:
        obj = get_object_or_404(Xmls, pk=q)
        file = os.path.join(settings.MEDIA_ROOT, str(obj.xml_file))
        fdir, fname = os.path.split(file)
        zf.write(file, fname)
    zf.close()

    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    resp[
        "Content-Disposition"
    ] = f"attachment; filename={datetime.datetime.today()}.rar"

    return resp


class XmlsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        if not bool(filter):
            today = datetime.date.today()

            first_month = f"{today.year}-{today.month}-01 00:00:00"
            today_formatted = f"{today} 23:59:59"

            filter = {
                "date_published__gte": first_month,
                "date_published__lte": today_formatted,
            }

        xmls = Xmls.objects.filter(**filter)

        senders = (
            Xmls.objects.filter(**filter)
            .values_list("sender", flat=True)
            .distinct()
            .order_by("sender")
        )

        serializer = XmlsResponseSerializer(xmls, many=True)

        response = {"senders": senders, "data": serializer.data}

        return Response(response, status.HTTP_200_OK)


class XmlsSendView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def post(self, request: Request, args=None) -> Response:
        cnpjs = [branch["cnpj"] for branch in Branches.objects.all().values("cnpj")]

        if args:
            files = args
        else:
            files = request.FILES.getlist("attachment[]")

        for file in files:
            try:
                document = minidom.parse(file)

            except AttributeError:
                s = io.BytesIO()
                s.write(file)
                s.seek(0)

                xml = s
                document = minidom.parseString(xml.getvalue())
                file = InMemoryUploadedFile(
                    xml,
                    field_name="xml",
                    name=f"{datetime.date.today()}.xml",
                    content_type="text/xml",
                    size=len(xml.getvalue()),
                    charset="UTF-8",
                )

            try:
                author = (
                    User.objects.get(id=1)
                    if request.user not in User.objects.all()
                    else request.user
                )
                destiny_cnpj = (
                    document.getElementsByTagName("dest")[0]
                    .getElementsByTagName("CNPJ")[0]
                    .firstChild.nodeValue
                )
                if destiny_cnpj not in cnpjs:
                    nf = document.getElementsByTagName("nNF")[0].firstChild.nodeValue
                    dhEmi = dateformat.format(
                        datetime.datetime.strptime(
                            document.getElementsByTagName("dhEmi")[
                                0
                            ].firstChild.nodeValue,
                            "%Y-%m-%dT%H:%M:%S%z",
                        ),
                        "Y-m-d H:i",
                    )
                    try:
                        rem = (
                            document.getElementsByTagName("emit")[0]
                            .getElementsByTagName("xFant")[0]
                            .firstChild.nodeValue
                        )
                    except IndexError:
                        rem = (
                            document.getElementsByTagName("emit")[0]
                            .getElementsByTagName("xNome")[0]
                            .firstChild.nodeValue
                        )
                    dest = (
                        document.getElementsByTagName("dest")[0]
                        .getElementsByTagName("xNome")[0]
                        .firstChild.nodeValue
                    )
                    dest_mun = (
                        document.getElementsByTagName("dest")[0]
                        .getElementsByTagName("xMun")[0]
                        .firstChild.nodeValue
                    )
                    dest_uf = (
                        document.getElementsByTagName("dest")[0]
                        .getElementsByTagName("UF")[0]
                        .firstChild.nodeValue
                    )
                    dest_bairro = (
                        document.getElementsByTagName("dest")[0]
                        .getElementsByTagName("xBairro")[0]
                        .firstChild.nodeValue
                    )
                    dest_cep = (
                        document.getElementsByTagName("dest")[0]
                        .getElementsByTagName("CEP")[0]
                        .firstChild.nodeValue
                    )
                    peso = (
                        document.getElementsByTagName("transp")[0]
                        .getElementsByTagName("pesoB")[0]
                        .firstChild.nodeValue
                    )
                    volume = (
                        document.getElementsByTagName("transp")[0]
                        .getElementsByTagName("qVol")[0]
                        .firstChild.nodeValue
                    )
                    vlr_nf = (
                        document.getElementsByTagName("total")[0]
                        .getElementsByTagName("vNF")[0]
                        .firstChild.nodeValue
                    )
                    skus = getText(document)

                    if skus:
                        try:
                            rom = Xmls.objects.create(
                                date_emission=dhEmi,
                                nf=nf,
                                sender=rem,
                                recipient=dest,
                                weight=peso,
                                volume=volume,
                                value_nf=vlr_nf,
                                district=dest_bairro,
                                cep=dest_cep,
                                county=dest_mun,
                                uf=dest_uf,
                                author=author,
                                xml_file=file,
                            )
                        except Exception as e:
                            print(f"Error: {e}, error_type: {type(e).__name__}")
                            raise e
                        else:
                            for q in skus:
                                Skus.objects.create(
                                    code=q["sku"],
                                    discount_product=q["descprod"],
                                    type_unity=q["un"],
                                    quantity_unity=int(q["qnt"]),
                                    type_volume=q["un2"],
                                    quantity_volume=int(q["qnt2"]),
                                    xml=rom,
                                )
                else:
                    pass
            except:
                continue

        return Response({}, status.HTTP_201_CREATED)


class XmlsSyncView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, BasePermission]

    def post(self, request: Request) -> Response:
        host = os.getenv("E_HOST_XML")
        user = os.getenv("E_MAIL_XML")
        password = os.getenv("E_PASS_XML")

        pp = poplib.POP3(host)
        pp.set_debuglevel(1)
        pp.user(user)
        pp.pass_(password)

        xmls = []
        num_messages = len(pp.list()[1])
        for i in range(num_messages):
            raw_email = b"\n".join(pp.retr(i + 1)[1])
            parsed_mail = email.message_from_bytes(raw_email)
            if parsed_mail.is_multipart():
                for part in parsed_mail.walk():
                    filename = part.get_filename()
                    if re.findall(re.compile(r"\w+(?i:.xml|.XML)"), str(filename)):
                        xmls.extend({part.get_payload(decode=True)})
            pp.dele(i + 1)
        pp.quit()

        try:
            XmlsSendView.post(self, request, args=xmls)
        except Exception as e:
            return Response({"error": e.args}, status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Ok"}, status.HTTP_201_CREATED)


class XmlsDownloadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def post(self, request: Request) -> Response:
        rom_id = request.data.getlist("list_rom_id[]")
        type_download = request.data.get("type_download")

        if rom_id:
            if type_download == "COMPLETO":
                romaneio = Skus.objects.filter(xml__id__in=rom_id).annotate(
                    nf1=F("xml__nf"),
                    municipio1=F("xml__county"),
                    uf1=F("xml__uf"),
                    codigo1=F("code"),
                    qnt_un1=F("quantity_unity"),
                    desc_prod1=F("discount_product"),
                    rem=F("xml__sender"),
                    romaneio_id=F("xml_id"),
                    volume=F("xml__volume"),
                )
            elif type_download == "SIMPLES":
                romaneio = Xmls.objects.filter(id__in=rom_id).annotate(
                    nf1=F("nf"),
                    volume1=F("volume"),
                    uf1=F("uf"),
                    rem=F("sender"),
                )
            elif type_download == "REMETENTE":
                romaneio = Skus.objects.filter(xml__id__in=rom_id).annotate(
                    municipio1=F("xml__county"),
                    uf1=F("xml__uf"),
                    codigo1=F("code"),
                    qnt_un1=F("quantity_unity"),
                    desc_prod1=F("discount_product"),
                    rem=F("xml__sender"),
                    romaneio_id=F("xml__nf"),
                    volume=F("xml__volume"),
                    valor=F("xml__value_nf"),
                    tp_un1=F("type_unity"),
                    peso=F("xml__weight"),
                    tp_vol1=F("type_volume"),
                    qnt_vol1=F("quantity_volume"),
                )
            elif type_download == "DESTINATÁRIO":
                romaneio = Skus.objects.filter(xml__id__in=rom_id).annotate(
                    municipio1=F("xml__county"),
                    uf1=F("xml__uf"),
                    codigo1=F("code"),
                    qnt_un1=F("quantity_unity"),
                    desc_prod1=F("discount_product"),
                    dest=F("xml__recipient"),
                    romaneio_id=F("xml__nf"),
                    volume=F("xml__volume"),
                    valor=F("xml__value_nf"),
                    tp_un1=F("type_unity"),
                    peso=F("xml__weight"),
                    tp_vol1=F("type_volume"),
                    qnt_vol1=F("quantity_volume"),
                    bairro1=F("xml__district"),
                    cep1=F("xml__cep"),
                )
            elif type_download == "XMLS":
                try:
                    rar = getFiles(*rom_id)
                except Exception as e:
                    raise e
                if rar:
                    return rar
            else:
                return Response(
                    {
                        "message": "Selecione o tipo de download.",
                        "field": "type_download",
                    },
                    status.HTTP_400_BAD_REQUEST,
                )
            try:
                if romaneio:
                    sheet = rom_xml_to_excel(*romaneio, type_download=type_download)
                else:
                    pass
            except KeyError:
                return Response(
                    {"message": "Não encontrado valores para sua solicitação."},
                    status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                print(e, type(e).__name__)
                return Response(
                    {"message": "Algo deu errado, verifique e tente novamente."},
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            else:
                if sheet:
                    return sheet


def rom_xml_to_excel(*romaneio, type_download):
    array = []
    roms = []
    for q in romaneio:
        if type_download == "COMPLETO":
            array.append(
                {
                    "nf": q.nf1,
                    "municipio": q.municipio1,
                    "uf": q.uf1,
                    "codigo": q.codigo1,
                    "qnt_un": q.qnt_un1,
                    "desc": q.desc_prod1,
                    "remetente": q.rem,
                    "ref_id": q.romaneio_id,
                    "volume": q.volume,
                }
            )
            if q.romaneio_id not in roms:
                roms.extend({q.romaneio_id})
        elif type_download == "SIMPLES":
            array.append({"nf": q.nf1, "uf": q.uf1, "volume": q.volume})
            if q.id not in roms:
                roms.extend({q.id})
        elif type_download == "REMETENTE":
            array.append(
                {
                    "municipio": q.municipio1,
                    "uf": q.uf1,
                    "codigo": q.codigo1,
                    "qnt_un": q.qnt_un1,
                    "desc": q.desc_prod1,
                    "remetente": q.rem,
                    "nota": q.romaneio_id,
                    "volume": q.volume,
                    "valor": q.valor,
                    "tp_un": q.tp_un1,
                    "peso": q.peso,
                    "tp_vol": q.tp_vol1,
                    "qnt_vol": q.qnt_vol1,
                }
            )
            if q.romaneio_id not in roms:
                roms.extend({q.romaneio_id})
        elif type_download == "DESTINATÁRIO":
            array.append(
                {
                    "municipio": q.municipio1,
                    "uf": q.uf1,
                    "codigo": q.codigo1,
                    "qnt_un": q.qnt_un1,
                    "desc": q.desc_prod1,
                    "destinatario": q.dest,
                    "nota": q.romaneio_id,
                    "volume": q.volume,
                    "valor": q.valor,
                    "tp_un": q.tp_un1,
                    "peso": q.peso,
                    "tp_vol": q.tp_vol1,
                    "qnt_vol": q.qnt_vol1,
                    "bairro": q.bairro1,
                    "cep": q.cep1,
                }
            )
            if q.romaneio_id not in roms:
                roms.extend({q.romaneio_id})
    Xmls.objects.filter(pk__in=roms).update(printed=True)
    pdr = pd.DataFrame(array)
    if type_download == "COMPLETO":
        dt = (
            pdr.pivot_table(
                index=["codigo", "desc"],
                columns=["uf"],
                values=["qnt_un"],
                aggfunc=np.sum,
                fill_value="0",
                margins=True,
                margins_name="Total",
            )
        ).astype(np.int64)
    elif type_download == "SIMPLES":
        dt = (
            pdr.pivot_table(
                index=["nf"],
                columns=["uf"],
                values=["volume"],
                aggfunc=np.sum,
                fill_value="0",
                margins=True,
                margins_name="Total",
            )
        ).astype(np.int64)
    elif type_download == "REMETENTE":
        dt = (
            pdr.pivot_table(
                index=[
                    "remetente",
                    "nota",
                    "valor",
                    "peso",
                    "desc",
                    "tp_un",
                    "tp_vol",
                ],
                values=["qnt_un", "qnt_vol"],
                fill_value="0",
            )
        ).astype(np.float32)
    elif type_download == "DESTINATÁRIO":
        dt = (
            pdr.pivot_table(
                index=[
                    "destinatario",
                    "nota",
                    "volume",
                    "valor",
                    "peso",
                    "bairro",
                    "cep",
                    "desc",
                    "tp_un",
                    "tp_vol",
                ],
                values=["qnt_un", "qnt_vol"],
                fill_value="0",
            )
        ).astype(np.float32)
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="report.xlsx"'
    # ] = f'attachment; filename="{datetime.date.today().strftime("%d/%m/%Y")}.xlsx"'
    writer = pd.ExcelWriter(response, engine="xlsxwriter")
    dt.to_excel(writer, "Dinamica")
    pdr.to_excel(writer, "Relatorio")
    writer.close()

    try:
        if response:
            return response
    except Exception as e:
        raise e
