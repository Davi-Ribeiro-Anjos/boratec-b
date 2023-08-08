from django.urls import path

from . import views

urlpatterns = [
    path(
        "employees/",
        views.EmployeesView.as_view(),
        name="employees",
    ),
    path(
        "employees/<int:id>/",
        views.EmployeesDetailView.as_view(),
        name="employees-id",
    ),
    path(
        "employees/choices/",
        views.EmployeesChoicesView.as_view(),
        name="employees-choices",
    ),
]
