from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Branches
from .serializers import BranchesSerializer


class BranchesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        branches = Branches.objects.all()
        serializer = BranchesSerializer(branches, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = BranchesSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        filial = Branches.objects.create(**serializer.validated_data)

        serializer = BranchesSerializer(filial)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
