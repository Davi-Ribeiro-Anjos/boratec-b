import csv
from datetime import date, datetime, timedelta
from jwt.exceptions import DecodeError

from _app import settings
from _service.token import create_token_email, decode_token_email

from rest_framework.views import APIView, Response, Request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.http import FileResponse

from tokens_emails.models import TokensEmails

from .models import VacanciesControls
from .serializers import (
    VacanciesControlsSerializer,
    VacanciesControlsResponseSerializer,
    VacanciesControlsEmailsSerializer,
)
from .permissions import MainPermission, AdminPermission


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


class VacanciesExportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def post(self, request: Request) -> Response:
        try:
            data = request.data.dict()
        except:
            data = request.data

        vacancies = VacanciesControls.objects.filter(**data)

        with open(
            "Relatório de Vagas.csv", "w", newline="", encoding="latin-1"
        ) as csv_file:
            fieldnames = [
                "ALERTA",
                "TÍTULO",
                "TIPO DE VAGA",
                "SOLICITANTE",
                "RECRUTADOR",
                "EMPRESA",
                "FILIAL",
                "MOTIVO",
                "INICIATIVA",
                "QUANTIDADE",
                "SELECIONADO",
                "STATUS",
                "OBSERVAÇÃO",
                "DATA DE SOLICITAÇÃO",
                "DATA DE ADMISSÃO",
                "DATA DE LIMITE",
                "DATA DO VETTA",
                "DATA DO EXAME",
                "DATA DE FECHAMENTO",
            ]

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

            writer.writeheader()

            today = date.today()

            for vacancy in vacancies:
                if today <= vacancy.date_requested + timedelta(days=15):
                    alert = "VERDE"
                else:
                    alert = "VERMELHO"

                writer.writerow(
                    {
                        "ALERTA": alert,
                        "TÍTULO": vacancy.title,
                        "TIPO DE VAGA": vacancy.type_vacancy,
                        "SOLICITANTE": vacancy.author.name,
                        "RECRUTADOR": vacancy.recruiter,
                        "EMPRESA": vacancy.company,
                        "FILIAL": vacancy.branch.abbreviation,
                        "MOTIVO": vacancy.motive,
                        "INICIATIVA": vacancy.initiative,
                        "QUANTIDADE": vacancy.quantity,
                        "SELECIONADO": vacancy.selected,
                        "STATUS": vacancy.status,
                        "OBSERVAÇÃO": vacancy.observation,
                        "DATA DE SOLICITAÇÃO": vacancy.date_requested,
                        "DATA DE ADMISSÃO": vacancy.date_expected_start,
                        "DATA DE LIMITE": vacancy.date_limit,
                        "DATA DO VETTA": vacancy.date_vetta,
                        "DATA DO EXAME": vacancy.date_exam,
                        "DATA DE FECHAMENTO": vacancy.date_closed,
                    }
                )

        file_csv = FileResponse(
            open("Relatório de Vagas.csv", "rb"),
            content_type="text/csv",
        )

        return file_csv


class VacanciesEmailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, MainPermission]

    def post(self, request: Request) -> Response:
        data = request.data

        vacancy = get_object_or_404(VacanciesControls, id=data["id"])

        serializer = VacanciesControlsEmailsSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(vacancy, key, value)

        verify_email_to_send(vacancy)

        vacancy.save()

        return Response({"message": "E-mail enviado com sucesso."}, status.HTTP_200_OK)


class VacanciesEmailsConfirmView(APIView):
    def patch(self, request: Request) -> Response:
        data = request.data

        token = data["token"]
        try:
            dict_token = decode_token_email(token)
        except DecodeError:
            return Response(
                {"message": "Autenticação incorreta."}, status.HTTP_400_BAD_REQUEST
            )

        token = get_object_or_404(TokensEmails, token=token)

        now = datetime.now()
        date_emission = token.date_emission
        date_expiration = token.date_expiration

        if now > date_emission and now < date_expiration:
            for key, _ in dict_token.items():
                if "email_" in key:
                    role = key.replace("email_", "")

                    break

            vacancy = get_object_or_404(VacanciesControls, id=dict_token["identifier"])

            if bool(data["approval"]):
                vacancy.__setattr__(f"approval_{role}", "APROVADO")
            else:
                vacancy.__setattr__(f"approval_{role}", "REPROVADO")
                vacancy.__setattr__(f"comment_{role}", data["comment"])

                vacancy.status = "REPROVADO"

                vacancy.save()

                return Response({}, status.HTTP_204_NO_CONTENT)

            vacancy.__setattr__(f"comment_{role}", data["comment"])

            verify_email_to_send(vacancy)

            vacancy.save()

            return Response({}, status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "Autenticação expirada."}, status.HTTP_400_BAD_REQUEST
            )


def verify_email_to_send(vacancy: VacanciesControls):
    send = True
    if not vacancy.approval_manager == "APROVADO" and vacancy.email_manager:
        vacancy.email_send_manager = True
        send_to = vacancy.email_manager
        attribute = "email_manager"

    elif (
        (
            vacancy.approval_regional_manager == "NÃO RESPONDIDO"
            and vacancy.approval_manager == "APROVADO"
        )
        or (
            not bool(vacancy.email_manager)
            and vacancy.approval_manager == "NÃO RESPONDIDO"
            and not vacancy.approval_regional_manager == "APROVADO"
        )
    ) and bool(vacancy.email_regional_manager):
        vacancy.email_send_regional_manager = True
        send_to = vacancy.email_regional_manager
        attribute = "email_regional_manager"

    elif (
        (
            vacancy.approval_rh == "NÃO RESPONDIDO"
            and vacancy.approval_regional_manager == "APROVADO"
        )
        or (
            not bool(vacancy.email_regional_manager)
            and vacancy.approval_regional_manager == "NÃO RESPONDIDO"
            and not vacancy.approval_rh == "APROVADO"
        )
    ) and bool(vacancy.email_rh):
        vacancy.email_send_rh = True
        send_to = vacancy.email_rh
        attribute = "email_rh"

    elif (
        (
            vacancy.approval_director == "NÃO RESPONDIDO"
            and vacancy.approval_rh == "APROVADO"
        )
        or (
            not bool(vacancy.email_rh)
            and vacancy.approval_rh == "NÃO RESPONDIDO"
            and not vacancy.approval_director == "APROVADO"
        )
    ) and bool(vacancy.email_director):
        vacancy.email_send_director = True
        send_to = vacancy.email_director
        attribute = "email_director"

    else:
        send = False

    if send:
        dict_to_token = {
            "identifier": vacancy.id,
            "title": vacancy.title,
            "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        dict_to_token[attribute] = send_to

        token = create_token_email(dict_to_token)

        date_expiration = datetime.now() + timedelta(hours=24)

        obj = {
            "email": send_to,
            "token": token,
            "date_expiration": date_expiration,
        }

        TokensEmails.objects.create(**obj)

        params = {
            "title": vacancy.title,
            "salary_range": vacancy.salary_range,
            "role": vacancy.role.name,
            "branch": vacancy.branch.abbreviation,
            "company": vacancy.company,
            "author": vacancy.author.name,
            "link": f"https://bora.tec.br/vaga/{token}/",
        }

        render = settings.TEMPLATE_ENV.get_template("email/vacancy.html").render(
            **params
        )

        send_mail(
            subject=f"Abertura de Vaga - {vacancy.title}",
            message="Abertura de Vaga",
            html_message=render,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[send_to],
            fail_silently=False,
        )

        vacancy.__setattr__(attribute.replace("email", "email_send"), True)
        vacancy.status = "EM ANDAMENTO"

    else:
        vacancy.status = "APROVADO"
