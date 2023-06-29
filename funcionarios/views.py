from rest_framework.views import APIView, Response, Request, status

from django.shortcuts import get_object_or_404

from pj_complementos.models import PJComplementos

from .models import Funcionarios
from .serializers import FuncionariosSerializer, FuncionariosResponseSerializer


class FuncionariosView(APIView):
    def get(self, request: Request) -> Response:
        funcionarios = Funcionarios.objects.all()
        serializer = FuncionariosResponseSerializer(funcionarios, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        # data["complemento_funcionario"] = PJComplementos.objects.filter(
        #     id=data["complemento_funcionario"]
        # ).first()

        serializer = FuncionariosSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        funcionario = Funcionarios.objects.create(**serializer.validated_data)

        serializer = FuncionariosResponseSerializer(funcionario)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


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
