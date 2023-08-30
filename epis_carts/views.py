from django.db import IntegrityError
from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from epis_carts.models import EPIsCarts
from epis_carts.serializers import EPIsCartsSerializer
from epis_sizes.models import EPIsSizes

from .models import EPIsCarts
from .serializers import (
    EPIsCartsSerializer,
    EPIsCartsResponseSerializer,
)

from .permissions import BasePermission


class EPIsCartsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request) -> Response:
        carts = EPIsCarts.objects.all()

        serializer = EPIsCartsResponseSerializer(carts, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    # def post(self, request: Request) -> Response:
    #     try:
    #         data = request.data.dict()
    #     except:
    #         data = request.data

    #     list_items = data["items"]

    #     for item in list_items:
    #         size = EPIsSizes.objects.get(id=item["size"])

    #         try:
    #             size.quantity_provisory -= int(item["quantity"])
    #             size.save()
    #         except IntegrityError as e:
    #             return Response(
    #                 {
    #                     "message": f"Insira uma quantidade menor em {size.item.description}"
    #                 },
    #                 status.HTTP_400_BAD_REQUEST,
    #             )
    #         except Exception as e:
    #             return Response(e.args, status.HTTP_400_BAD_REQUEST)

    #     serializer = EPIsCartsSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)

    #     req: EPIsCarts = EPIsCarts.objects.create(**serializer.validated_data)

    #     for item in list_items:
    #         item["request"] = req.id

    #         serializer = EPIsCartsSerializer(data=item)
    #         serializer.is_valid(raise_exception=True)

    #         EPIsCarts.objects.create(**serializer.validated_data)

    #     serializer = EPIsCartsResponseSerializer(req)

    #     return Response(serializer.data, status.HTTP_201_CREATED)
