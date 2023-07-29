from rest_framework.views import APIView, Response, Request, status

from .models import Filiais
from .serializers import FiliaisSerializer


class FiliaisView(APIView):
    def get(self, request: Request) -> Response:
        filiais = Filiais.objects.all()
        serializer = FiliaisSerializer(filiais, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = FiliaisSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        filial = Filiais.objects.create(**serializer.validated_data)

        serializer = FiliaisSerializer(filial)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
