import io
import os
import email
import datetime
import poplib

from xml.dom import minidom
from asgiref.sync import sync_to_async

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.utils import dateformat

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from employees.models import Employees
from skus.models import Skus

from .models import Xmls
from .serializers import (
    XmlsSerializer,
    XmlsResponseSerializer,
)
from .permissions import BasePermission


class XmlsView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        xmls = Xmls.objects.all()

        serializer = XmlsResponseSerializer(xmls, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class XmlsSendView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, BasePermission]

    @sync_to_async
    def post(self, request: Request, args=None) -> Response:
        cnpjs = [
            "05504835000100",
            "05504835000283",
            "05504835000526",
            "05504835000364",
            "05504835000607",
            "05504835000445",
            "05504835000798",
            "05504835000879",
            "05504835000950",
            "05504835001093",
            "14059252000109",
            "14059252000281",
            "14059252000443",
            "14059252000362",
            "14059252000524",
            "44536137000130",
            "44536137000211",
            "44536137000300",
            "44536137000483",
            "44536137000564",
            "44536137000645",
            "44536137000726",
            "44536137000807",
            "44329445000195",
            "44326860000195",
            "44307910000197",
            "44307936000135",
            "36995897000188",
        ]

        if args:
            files = args
        else:
            files = request.FILES.getlist("xmls")

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
                                xml=file,
                            )
                        except Exception as e:
                            print(f"Error: {e}, error_type: {type(e).__name__}")
                            raise e
                        else:
                            for q in skus:
                                Skus.objects.create(
                                    code=q["sku"],
                                    description=q["descprod"],
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

    async def post(self, request: Request) -> Response:
        host = os.environ.get("E_HOST_XML")
        user = os.environ.get("E_MAIL_XML")
        password = os.environ.get("E_PASS_XML")

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
            # print(f"ARRAY XML: LEN({len(xmls)})")
            await XmlsSendView.post(request, args=xmls)
        except Exception as e:
            # print(f"Error: {e}, error_type: {type(e).__name__}")
            return Response({"error": e.message}, status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Ok"}, status.HTTP_201_CREATED)


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
