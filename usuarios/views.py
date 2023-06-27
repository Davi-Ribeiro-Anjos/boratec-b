from rest_framework.views import APIView, Response, Request, status

from django.contrib.auth.models import User

from .serializers import UsuariosSimplesSerializer


class UsuariosView(APIView):
    def get(self, request: Request) -> Response:
        usuarios = User.objects.all()
        serializer = UsuariosSimplesSerializer(usuarios, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
