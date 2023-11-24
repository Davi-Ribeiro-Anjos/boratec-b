from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from _app import settings

from .models import PJThirteenths
from .serializers import (
    PJThirteenthsSerializer,
    PJThirteenthsResponseSerializer,
)
from .permissions import AdminPermission


class PJThirteenthsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        if "send" in filter:
            if filter["send"] == "false":
                filter["send"] = False
            elif filter["send"] == "true":
                filter["send"] = True

        thirteenths = PJThirteenths.objects.filter(**filter).order_by("date_payment")

        serializer = PJThirteenthsResponseSerializer(thirteenths, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = PJThirteenthsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        thirteenth = PJThirteenths.objects.create(**serializer.validated_data)

        serializer = PJThirteenthsResponseSerializer(thirteenth)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PJThirteenthsDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def patch(self, request: Request, id: int) -> Response:
        thirteenth = get_object_or_404(PJThirteenths, id=id)

        serializer = PJThirteenthsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(thirteenth, key, value)

        thirteenth.save()

        serializer = PJThirteenthsResponseSerializer(thirteenth)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PJThirteenthsSendView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def post(self, request: Request) -> Response:
        try:
            data = request.data["ids"].dict()
        except:
            data = request.data["ids"]

        list_error = []

        for id in data:
            thirteenth = get_object_or_404(PJThirteenths, id=id)

            cnpj = thirteenth.employee.cnpj
            formatted_cnpj = (
                f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
            )

            if thirteenth.type_payment == "ADIANTAMENTO":
                title = "Adiantamento do 13º Salário."
            else:
                title = "Pagamento do 13º Salário."

            text = f"""Informações sobre o {"Adiantamento" if thirteenth.type_payment == "ADIANTAMENTO" else "Pagamento"} do 13º Salário.

    Valor do 13º: R$ {thirteenth.value:.2f}
    Data de Pagamento: {thirteenth.date_payment.strftime("%d/%m/%Y")}
    Serviço Prestado em: {thirteenth.employee.branch.abbreviation} - {thirteenth.employee.branch.uf}
    Dados Bancários: 
        Banco : {thirteenth.employee.bank}
        Ag    : {thirteenth.employee.agency}
        C.c.  : {thirteenth.employee.account}
    CNPJ: {formatted_cnpj}
    PIX: {thirteenth.employee.pix or "Não Informado"}

Favor enviar a NF até {request.data["date_emission"]}.

Att, Departamento Pessoal
                    """
            try:
                send_mail(
                    subject=title,
                    message=text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[
                        thirteenth.employee.email,
                        "lucas.feitosa@bora.com.br",
                    ],
                    fail_silently=False,
                )

                thirteenth.send = True

                thirteenth.save()

            except Exception as e:
                serializer = PJThirteenthsResponseSerializer(thirteenth)

                list_error.append(serializer.data)

        if len(list_error) > 0:
            return Response(list_error, status.HTTP_400_BAD_REQUEST)

        return Response({}, status.HTTP_204_NO_CONTENT)
