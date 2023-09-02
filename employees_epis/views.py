from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404

from employees.models import Employees

from .models import EmployeesEPIs
from .serializers import (
    EmployeesEPIsSerializer,
)
from .permissions import BasePermission


class EmployeesEPIsDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BasePermission]

    def get(self, request: Request, employee_id: int) -> Response:
        employee = get_object_or_404(Employees, id=employee_id)

        epi = employee.epi

        serializer = EmployeesEPIsSerializer(epi)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request, employee_id: int) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        employee = get_object_or_404(Employees, id=employee_id)

        try:
            if employee.epi is None:
                raise Exception(e)

            epi = EmployeesEPIs.objects.get(id=employee.epi.id)

            serializer = EmployeesEPIsSerializer(data=data, partial=True)
            serializer.is_valid(raise_exception=True)

            for key, value in serializer.validated_data.items():
                setattr(epi, key, value)

            epi.save()

            serializer = EmployeesEPIsSerializer(epi)

            return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            serializer = EmployeesEPIsSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            epi = EmployeesEPIs.objects.create(**serializer.validated_data)

            employee.epi = epi

            employee.save()

            serializer = EmployeesEPIsSerializer(epi)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
