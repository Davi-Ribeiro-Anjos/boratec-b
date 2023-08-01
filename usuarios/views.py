import jwt
from _app.settings import SECRET_KEY

from rest_framework.views import APIView, Response, Request, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken


from django.contrib.auth.models import User


from _service.jwt import custom_payload_handler
from .serializers import UsuariosSimplesSerializer


class UsuariosView(APIView):
    def get(self, request: Request) -> Response:
        usuarios = User.objects.all()
        serializer = UsuariosSimplesSerializer(usuarios, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            pass
            # token = response.data["access"]
            # token_dict = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # print(token_dict, "\n\n")
            # response.data["access"] = custom_payload_handler(token_dict)
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            pass
            # token = response.data["access"]
            # token_dict = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # response.data["access"] = custom_payload_handler(token_dict)
        return response
