from django.db import IntegrityError, DataError
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from epis_carts.models import EPIsCarts
from epis_carts.serializers import EPIsCartsSerializer
from epis_sizes.models import EPIsSizes
from _app import settings

from .models import EPIsRequests
from .serializers import (
    EPIsRequestsSerializer,
    EPIsRequestsResponseSerializer,
)
from .permissions import BasePermission


class EPIsRequestsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        requests = EPIsRequests.objects.filter(**filter)

        serializer = EPIsRequestsResponseSerializer(requests, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        list_items = data["items"]

        if data["status"] != "PROVISORIO":
            for item in list_items:
                size = EPIsSizes.objects.get(id=item["size"])

                try:
                    size.quantity_provisory -= int(item["quantity"])
                    size.save()
                except IntegrityError as e:
                    return Response(
                        {
                            "message": f"Insira uma quantidade menor em {size.item.description}"
                        },
                        status.HTTP_400_BAD_REQUEST,
                    )
                except Exception as e:
                    return Response(e.args, status.HTTP_400_BAD_REQUEST)

        serializer = EPIsRequestsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        req: EPIsRequests = EPIsRequests.objects.create(**serializer.validated_data)

        for item in list_items:
            item["request"] = req.id

            serializer = EPIsCartsSerializer(data=item)
            serializer.is_valid(raise_exception=True)

            EPIsCarts.objects.create(**serializer.validated_data)

        serializer = EPIsRequestsResponseSerializer(req)

        return Response(serializer.data, status.HTTP_201_CREATED)


class EPIsRequestsCancelView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def patch(self, request: Request, id: int) -> Response:
        req = get_object_or_404(EPIsRequests, id=id)

        serializer = EPIsRequestsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(req, key, value)

        req.save()

        if req.status != "PROVISORIO":
            for cart in req.epis_carts.all():
                size = EPIsSizes.objects.get(id=cart.size.id)

                size.quantity_provisory += cart.quantity
                size.save()

        serializer = EPIsRequestsResponseSerializer(req)

        return Response(serializer.data, status.HTTP_201_CREATED)


class EPIsRequestsDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def patch(self, request: Request, id: int) -> Response:
        req = get_object_or_404(EPIsRequests, id=id)

        serializer = EPIsRequestsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(req, key, value)

        if req.status == "ANDAMENTO":
            try:
                for cart in req.epis_carts.all():
                    size = EPIsSizes.objects.get(id=cart.size.id)

                    size.quantity -= cart.quantity
                    size.save()

                    if size.quantity < size.quantity_minimum:
                        send_mail(
                            subject="Informação sobre quantidade mínima de estoque",
                            message=f"""Olá,
Informamos que o seguinte item atingiu a quantidade de estoque mínimo:

    ITEM: {size.item.description}
    CA: {size.item.ca}
    TAMANHO: {size.size}
    QUANTIDADE ATUAL: {size.quantity}
    QUANTIDADE MÍNIMA: {size.quantity_minimum}
                
Att, Equipe de Desenvolvimento
""",
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[
                                "rosane.fernandes@bora.com.br",
                                "daniel.domingues@bora.com.br",
                                "marco.antonio@bora.bom.br",
                                "lucas.franco@bora.bom.br",
                            ],
                            fail_silently=False,
                        )

            except IntegrityError:
                return Response(
                    {
                        "message": f"Não tem a quantidade do item {size.item.description} em estoque."
                    },
                    status.HTTP_400_BAD_REQUEST,
                )
            except DataError:
                return Response(
                    {
                        "message": f"Não tem a quantidade do item {size.item.description} em estoque."
                    },
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            except Exception as e:
                print(e)
                pass
            else:
                text = ""

                for cart in req.epis_carts.all():
                    text += f"      ITEM: {cart.size.item.description}\n"
                    text += f"      TAMANHO: {cart.size.size}\n"
                    text += f"      QUANTIDADE: {cart.quantity}\n\n"
                try:
                    send_mail(
                        subject="Envio de EPI",
                        message=f"""
Esse e-mail é referente ao do seu(s) EPI(s).

Esses são os dados da entrega:

    MOTORISTA: {request.data["driver"] if request.data["driver"] else "NÃO INFORMADO"}
    PLACA DO VEÍCULO: {request.data["vehicle_plate"] if request.data["vehicle_plate"] else "NÃO INFORMADO"}
    ITEMS:
        
{text}

OBSERVAÇÃO: {request.data["body_email"] if request.data["body_email"] else "SEM REGISTRO."}

Att, Equipe de Desenvolvimento
""",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[
                            request.data["email"],
                            "rosane.fernandes@bora.com.br",
                            "daniel.domingues@bora.com.br",
                            "marco.antonio@bora.bom.br",
                            "lucas.franco@bora.bom.br",
                        ],
                        fail_silently=False,
                    )
                except Exception as e:
                    print("Envia email - ", e)

        req.save()

        serializer = EPIsRequestsResponseSerializer(req)

        return Response(serializer.data, status.HTTP_201_CREATED)
