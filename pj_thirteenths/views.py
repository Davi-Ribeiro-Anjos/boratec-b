from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView, Response, Request, status

from django.shortcuts import get_object_or_404

from employees.models import Employees

from .models import PJComplements
from .serializers import (
    PJComplementsSerializer,
    PJComplementsResponseSerializer,
)


class PJComplementsView(APIView):
    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = PJComplementsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        pj_complement = PJComplements.objects.create(**serializer.validated_data)

        serializer = PJComplementsResponseSerializer(pj_complement)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PJComplementsDetailView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        pj_complement = get_object_or_404(PJComplements, id=id)

        serializer = PJComplementsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(pj_complement, key, value)

        pj_complement.save()

        serializer = PJComplementsResponseSerializer(pj_complement)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PJComplementsAddView(APIView):
    def post(self, request: Request) -> Response:
        employees = Employees.objects.filter(type_contract="PJ")

        for employee in employees:
            if not employee.pj_complements:
                data = {
                    "salary": 0,
                }

                pj_complement = PJComplements.objects.create(**data)

                employee.pj_complements = pj_complement
                employee.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
