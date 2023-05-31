from rest_framework.views import APIView, Response, Request, status

from .models import Filiais
from .serializers import FiliaisSerializer


class FiliaisView(APIView):
    def get(self, request: Request) -> Response:
        filiais = Filiais.objects.all()
        serializer = FiliaisSerializer(filiais, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
