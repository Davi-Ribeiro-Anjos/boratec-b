from django.core.exceptions import ValidationError

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from epis_carts.models import EPIsCarts
from epis_carts.serializers import EPIsCartsSerializer
from epis_sizes.models import EPIsSizes

from _service.limit_size import file_size

from .models import Routes
from .serializers import (
    RoutesSerializer,
    RoutesResponseSerializer,
)


class RoutesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        manuals = Routes.objects.filter(**filter)
        systems = Routes.objects.all().values("system").distinct()

        serializer = RoutesResponseSerializer(manuals, many=True)

        return Response(
            {"data": serializer.data, "systems": systems}, status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        file = request.FILES.get("file")
        try:
            file_size(file, 5)
        except ValidationError as e:
            return Response({"message": e.args[0]}, status.HTTP_400_BAD_REQUEST)

        serializer = RoutesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        manual = Routes.objects.create(**serializer.validated_data)

        serializer = RoutesResponseSerializer(manual)

        return Response(serializer.data, status.HTTP_201_CREATED)


class RoutesDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, id: int) -> Response:
        pass
