from rest_framework.views import APIView, Response, Request, status

from django.shortcuts import get_object_or_404

from .models import Funcionarios
from .serializers import FuncionariosSerializer, FuncionariosResponseSerializer


class FuncionariosView(APIView):
    def get(self, request: Request) -> Response:
        funcionarios = Funcionarios.objects.all()
        serializer = FuncionariosResponseSerializer(funcionarios, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class FuncionariosDetailView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        funcionario = get_object_or_404(Funcionarios, id=id)
        serializer = FuncionariosSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(funcionario, key, value)

        funcionario.save()

        serializer = FuncionariosResponseSerializer(funcionario)

        return Response(serializer.data, status.HTTP_201_CREATED)


class FuncionariosChoicesView(APIView):
    def get(self, request: Request) -> Response:
        funcionarios = Funcionarios.objects.all().values("id", "nome")
        choices = [
            {"funcionarios": funcionarios},
        ]

        return Response(choices, status.HTTP_200_OK)
