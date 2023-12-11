from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.VacanciesView.as_view(),
        name="vacancies",
    ),
    path(
        "<int:id>/",
        views.VacanciesDetailsView.as_view(),
        name="vacancies-id",
    ),
    path(
        "export/",
        views.VacanciesExportView.as_view(),
        name="vacancies-export",
    ),
    path(
        "emails/",
        views.VacanciesEmailsView.as_view(),
        name="vacancies-emails",
    ),
    path(
        "emails/confirm/",
        views.VacanciesEmailsConfirmView.as_view(),
        name="vacancies-emails-confirm",
    ),
]
