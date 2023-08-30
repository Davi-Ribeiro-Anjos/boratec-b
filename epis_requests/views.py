from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from epis_carts.models import EPIsCarts
from epis_carts.serializers import EPIsCartsSerializer
from epis_sizes.models import EPIsSizes

from .models import EPIsRequests
from .serializers import (
    EPIsRequestsSerializer,
    EPIsRequestsResponseSerializer,
)

import ipdb

# from .permissions import BasePermission


class EPIsRequestsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, id: int) -> Response:
        req = get_object_or_404(EPIsRequests, id=id)

        serializer = EPIsRequestsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(req, key, value)

        req.save()

        serializer = EPIsRequestsResponseSerializer(req)

        for cart in req.epis_carts.all():
            size = EPIsSizes.objects.get(id=cart.size.id)

            size.quantity_provisory += cart.quantity
            size.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class EPIsRequestsDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, id: int) -> Response:
        req = get_object_or_404(EPIsRequests, id=id)

        serializer = EPIsRequestsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(req, key, value)

        req.save()

        serializer = EPIsRequestsResponseSerializer(req)

        return Response(serializer.data, status.HTTP_201_CREATED)
