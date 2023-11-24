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
        "vacancies/emails/",
        views.VacanciesEmailsView.as_view(),
        name="vacancies-emails",
    ),
]
