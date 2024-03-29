from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db.models import Q
from django.shortcuts import get_object_or_404

from employees.models import Employees
from employees.serializers import EmployeesSimpleSerializer

from .models import EmployeesDismissals
from .serializers import (
    EmployeesDismissalsSerializer,
)
from .permissions import AdminPermission


class EmployeesDismissalsCheckView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def get(self, request: Request, identity: int) -> Response:
        try:
            employee = Employees.objects.filter(
                (Q(cnpj=identity) | Q(cpf=identity)) & Q(status="DEMITIDO")
            ).order_by("-date_admission")[0]

            serializer = EmployeesSimpleSerializer(employee)

            return Response(serializer.data, status.HTTP_200_OK)
        except IndexError as e:
            return Response(
                {"error": "Funcionário não encontrado"}, status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Ocorreu um problema interno"},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EmployeesDismissalsDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def post(self, request: Request, employee_id: int) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        employee = get_object_or_404(Employees, id=employee_id)

        serializer = EmployeesDismissalsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        dismissal = EmployeesDismissals.objects.create(**serializer.validated_data)

        employee.dismissal = dismissal

        employee.save()

        serializer = EmployeesDismissalsSerializer(dismissal)

        return Response(serializer.data, status.HTTP_201_CREATED)
