from django.core.exceptions import ValidationError

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from epis_carts.models import EPIsCarts
from epis_carts.serializers import EPIsCartsSerializer
from epis_sizes.models import EPIsSizes

from _service.limit_size import file_size

from .models import Manuals
from .serializers import (
    ManualsSerializer,
    ManualsResponseSerializer,
)


class ManualsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        manuals = Manuals.objects.filter(**filter)
        systems = Manuals.objects.all().values("system").distinct()
        modules = Manuals.objects.all().values("module").distinct()

        serializer = ManualsResponseSerializer(manuals, many=True)

        return Response(
            {"data": serializer.data, "systems": systems, "modules": modules},
            status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        file = request.FILES.get("file")
        try:
            file_size(file, 5)
        except ValidationError as e:
            return Response({"message": e.args[0]}, status.HTTP_400_BAD_REQUEST)

        serializer = ManualsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        manual = Manuals.objects.create(**serializer.validated_data)

        serializer = ManualsResponseSerializer(manual)

        return Response(serializer.data, status.HTTP_201_CREATED)


class ManualsDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, id: int) -> Response:
        pass
