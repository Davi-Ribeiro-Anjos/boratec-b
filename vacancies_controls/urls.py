from django.urls import path

from . import views

urlpatterns = [
    path(
        "vacancies/",
        views.VacanciesControlsView.as_view(),
        name="vacancies",
    ),
    path(
        "vacancies/<int:id>/",
        views.VacanciesDetailsView.as_view(),
        name="vacancies-id",
    ),
    path(
        "vacancies/export/",
        views.VacanciesExportView.as_view(),
        name="vacancies-export",
    ),
    path(
        "vacancies/emails/",
        views.VacanciesEmailsView.as_view(),
        name="vacancies-emails",
    ),
    path(
        "vacancies/emails/confirm/",
        views.VacanciesEmailsConfirmView.as_view(),
        name="vacancies-emails-confirm",
    ),
]
