from rest_framework.views import APIView, Response, Request, status

from .models import SolicitacoesCompras
from .serializers import SolicitacoesComprasSerializer


class SolicitacoesComprasView(APIView):
    def get(self, request: Request) -> Response:
        solicitacoes = SolicitacoesCompras.objects.all().order_by("-id")
        serializer = SolicitacoesComprasSerializer(solicitacoes, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = SolicitacoesComprasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        solicitacao = SolicitacoesCompras.objects.create(**serializer.validated_data)

        serializer = SolicitacoesComprasSerializer(solicitacao)

        return Response(serializer.data, status.HTTP_201_CREATED)
