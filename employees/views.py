from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404

from pj_complements.models import PJComplements

from .models import Employees
from .serializers import EmployeesSerializer, EmployeesResponseSerializer

import ipdb


class EmployeesView(APIView):
    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        employees = Employees.objects.filter(**filter).order_by("nome")

        serializer = EmployeesResponseSerializer(employees, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        # data["pj_complements"] = PJComplements.objects.filter(
        #     id=data["pj_complements"]
        # ).first()

        serializer = EmployeesSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        employee = Employees.objects.create(**serializer.validated_data)

        serializer = EmployeesResponseSerializer(employee)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class EmployeesDetailView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        employee = get_object_or_404(Employees, id=id)
        serializer = EmployeesSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(employee, key, value)

        employee.save()

        serializer = EmployeesResponseSerializer(employee)

        return Response(serializer.data, status.HTTP_201_CREATED)


class EmployeesChoicesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        employees = Employees.objects.all().values("id", "name")

        return Response(employees, status.HTTP_200_OK)
