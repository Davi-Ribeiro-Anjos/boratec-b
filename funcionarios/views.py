from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404

from pj_complementos.models import PJComplementos

from .models import Funcionarios
from .serializers import FuncionariosSerializer, FuncionariosResponseSerializer

import ipdb


class FuncionariosView(APIView):
    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        funcionarios = Funcionarios.objects.filter(**filter).order_by("nome")

        serializer = FuncionariosResponseSerializer(funcionarios, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        # data["pj_complementos"] = PJComplementos.objects.filter(
        #     id=data["pj_complementos"]
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        funcionarios = Funcionarios.objects.all().values("id", "nome")

        return Response(funcionarios, status.HTTP_200_OK)
