import jwt
import random
import string
import bcrypt
from _app import settings

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from _service.jwt import custom_payload_handler
from employees.models import Employees
from .serializers import UserSimpleSerializer, EmailSerializer

import ipdb


def random_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


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
            token_dict = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

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

        user = get_object_or_404(User, email=serializer.validated_data["email"])

        random_string = random_generator()

        salt = bcrypt.gensalt()

        hash_result = bcrypt.hashpw(random_string.encode("utf-8"), salt)

        user.forget = hash_result.decode("utf-8")

        try:
            send_mail(
                subject=f"Recuperação de Senha - {user.first_name.upper()}",
                message="Recuperação de Senha.",
                # html_message=render,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            user.save()

            Response({"message": "E-mail enviado com sucesso."}, status.HTTP_200_OK)
        except Exception as e:
            Response(
                {"message": "Ocorreu um erro ao enviar o e-mail."},
                status.HTTP_400_BAD_REQUEST,
            )


class SetPasswordView(APIView):
    def get(self, request: Request, email: str, token: str):
        try:
            data = request.data.dict()
        except:
            data = request.data

        serializer = EmailSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, email=serializer.validated_data["email"])

        random_string = random_generator()

        salt = bcrypt.gensalt()

        hash_result = bcrypt.hashpw(random_string.encode("utf-8"), salt)

        user.forget = hash_result.decode("utf-8")

        try:
            send_mail(
                subject=f"Recuperação de Senha - {user.first_name.upper()}",
                message=f"""Recuperação de Senha.
Token: {user.forget}
                """,
                # html_message=render,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            user.save()

            Response({"message": "E-mail enviado com sucesso."}, status.HTTP_200_OK)
        except Exception as e:
            Response(
                {"message": "Ocorreu um erro ao enviar o e-mail."},
                status.HTTP_400_BAD_REQUEST,
            )
