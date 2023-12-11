from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.EmployeesView.as_view(),
        name="employees",
    ),
    path(
        "payments/",
        views.EmployeesPaymentsView.as_view(),
        name="employees-payments",
    ),
    path(
        "<int:id>/",
        views.EmployeesDetailsView.as_view(),
        name="employees-id",
    ),
    path(
        "document/<int:id>/",
        views.EmployeesDocumentsView.as_view(),
        name="employees-document-id",
    ),
    path(
        "choices/",
        views.EmployeesChoicesView.as_view(),
        name="employees-choices",
    ),
]
