from _app import settings

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .models import VacanciesControls
from .serializers import (
    VacanciesControlsSerializer,
    VacanciesControlsResponseSerializer,
    VacanciesControlsEmailsSerializer,
)
from .permissions import MainPermission


class VacanciesControlsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, MainPermission]

    def get(self, request: Request) -> Response:
        filter = request.GET.dict()

        vehicles = VacanciesControls.objects.filter(**filter)
        serializer = VacanciesControlsResponseSerializer(vehicles, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = VacanciesControlsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vacancy = VacanciesControls.objects.create(**serializer.validated_data)

        serializer = VacanciesControlsResponseSerializer(vacancy)

        return Response(serializer.data, status.HTTP_201_CREATED)


class VacanciesDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, MainPermission]

    def patch(self, request: Request, id: int) -> Response:
        vacancy = get_object_or_404(VacanciesControls, id=id)

        serializer = VacanciesControlsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(vacancy, key, value)

        vacancy.save()

        serializer = VacanciesControlsResponseSerializer(vacancy)

        return Response(serializer.data, status.HTTP_204_NO_CONTENT)


class VacanciesEmailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, MainPermission]

    def patch(self, request: Request) -> Response:
        data = request.data

        vacancy = get_object_or_404(VacanciesControls, id=data["id"])

        serializer = VacanciesControlsEmailsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        render = settings.TEMPLATE_ENV.get_template("email/index.html").render()

        for key, value in serializer.validated_data.items():
            key_send = key.replace("email", "email_send")

            if not getattr(vacancy, key_send):
                send_mail(
                    subject=f"Abertura de Vaga - {vacancy.title}",
                    message="",
                    html_message=render,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[value],
                    fail_silently=False,
                )

                # setattr(vacancy, key_send, True)
                setattr(vacancy, key, value)

                vacancy.save()

                break

        return Response({}, status.HTTP_204_NO_CONTENT)
