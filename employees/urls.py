from django.urls import path

from . import views

urlpatterns = [
    path(
        "employees/",
        views.EmployeesView.as_view(),
        name="employees",
    ),
    path(
        "employees/payments/",
        views.EmployeesPaymentsView.as_view(),
        name="employees-payments",
    ),
    path(
        "employees/<int:id>/",
        views.EmployeesDetailsView.as_view(),
        name="employees-id",
    ),
    path(
        "employees/document/<int:id>/",
        views.EmployeesDocumentsView.as_view(),
        name="employees-document-id",
    ),
    path(
        "employees/choices/",
        views.EmployeesChoicesView.as_view(),
        name="employees-choices",
    ),
]
