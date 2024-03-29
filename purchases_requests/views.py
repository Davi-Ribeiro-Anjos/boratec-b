from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db.models import Q
from django.core.exceptions import FieldError, ValidationError
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from _app import settings
from _service.limit_size import file_size

from .models import (
    PurchasesRequests,
)
from .serializers import *
from .permissions import BasePermission, AdminPermission


class PurchasesRequestsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        params = request.GET.dict()
        list_params = [
            "number_request",
            "date_request",
            "date_request__gte",
            "date_request__lte",
            "requester",
            "requester__username",
            "status",
            "branch",
        ]

        wrong_params = [param for param in params if not param in list_params]
        if len(wrong_params) > 0:
            raise FieldError()

        try:
            if len(request.GET) > 0:
                if not "status" in params:
                    params["status__in"] = ["ABERTO", "ANDAMENTO"]
                    solicitation = PurchasesRequests.objects.filter(**params).order_by(
                        "date_request"
                    )

                solicitation = PurchasesRequests.objects.filter(**params).order_by(
                    "date_request"
                )
            else:
                solicitation = PurchasesRequests.objects.filter(
                    Q(status="ABERTO") | Q(status="ANDAMENTO")
                ).order_by("date_request")
        except FieldError:
            return Response(
                {
                    "message": "Parâmetros incorrretos",
                    "parametros_aceitos": [
                        "number_request",
                        "date_request",
                        "status",
                        "requester",
                        "branch",
                    ],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PurchasesRequestsResponseSerializer(solicitation, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        file = request.FILES.get("attachment")

        try:
            file_size(file, 5)
        except ValidationError as e:
            return Response({"message": e.args[0]}, status.HTTP_400_BAD_REQUEST)

        serializer = PurchasesRequestsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        solicitation = PurchasesRequests.objects.create(**serializer.validated_data)

        serializer = PurchasesRequestsResponseSerializer(solicitation)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PurchasesRequestsDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request, id: int) -> Response:
        solicitation = get_object_or_404(PurchasesRequests, id=id)

        serializer = PurchasesRequestsResponseSerializer(solicitation)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, id: int) -> Response:
        file = request.FILES.get("attachment")

        try:
            file_size(file, 5)
        except ValidationError as e:
            return Response({"message": e.args[0]}, status.HTTP_400_BAD_REQUEST)

        solicitation = get_object_or_404(PurchasesRequests, id=id)

        serializer = PurchasesRequestsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(solicitation, key, value)

        solicitation.save()

        try:
            entries = solicitation.purchases_entries.all()
            entries_string = (
                "\n".join(
                    [f"\nID - {entry.id}: \n{entry.observation}" for entry in entries]
                )
                if len(entries) > 0
                else "NÃO INFORMADO"
            )

            send_mail(
                subject=f"Ocorreu uma edição na solicitação {solicitation.number_request}.",
                message=f"""
        STATUS: {solicitation.status}
        SOLICITAÇÃO: {solicitation.number_request}
        CATEGORIA: {solicitation.category if solicitation.category == "" else "NÃO INFORMADO"}
        DATA: {solicitation.date_request.strftime("%d/%m/%Y")}
        RESPONSÁVEL: {solicitation.responsible.name if solicitation.responsible else "NÃO INFORMADO"}


        ENTRADAS:
    {entries_string}


        OBSERVAÇÃO:
    {solicitation.observation if solicitation.observation else "NÃO INFORMADO"}


        Atenciosamente,
        Bora Desenvolvimento.
                    """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[
                    solicitation.author.user.email,
                ],
                fail_silently=False,
            )
        except Exception as e:
            print(e)

        serializer = PurchasesRequestsResponseSerializer(solicitation)

        return Response(serializer.data, status.HTTP_204_NO_CONTENT)
