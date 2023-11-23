import jwt
from _app.settings import SECRET_KEY

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from _service.jwt import custom_payload_handler
from employees.models import Employees
from .serializers import UserSimpleSerializer, EmailSerializer

import ipdb


class UsersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request: Request) -> Response:
        users = User.objects.all()
        serializer = UserSimpleSerializer(users, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            token = response.data["access"]
            token_dict = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            response.data["access"] = custom_payload_handler(token_dict)
        return response


class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            pass
            # token = response.data["access"]
            # token_dict = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # response.data["access"] = custom_payload_handler(token_dict)
        return response


class ForgetPasswordView(APIView):
    def post(self, request: Request):
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = EmailSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        get_object_or_404(User, email=serializer.validated_data["email"])

        ipdb.set_trace()
