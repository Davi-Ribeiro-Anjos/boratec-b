from django.urls import path

from . import views

urlpatterns = [
    path(
        "check/<int:identity>/",
        views.EmployeesDismissalsCheckView.as_view(),
        name="employees-dismissals-check-identity",
    ),
    path(
        "<int:employee_id>/",
        views.EmployeesDismissalsDetailsView.as_view(),
        name="employees-dismissals-employee_id",
    ),
]
