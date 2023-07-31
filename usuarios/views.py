from rest_framework.views import APIView, Response, Request, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .serializers import UsuariosSimplesSerializer, LoginSerializer


class UsuariosView(APIView):
    def get(self, request: Request) -> Response:
        usuarios = User.objects.all()
        serializer = UsuariosSimplesSerializer(usuarios, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
