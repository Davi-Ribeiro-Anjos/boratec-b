from django.urls import path

from . import views

urlpatterns = [
    path(
        "employees-dismissals/check/<int:identity>/",
        views.EmployeesDismissalsCheckView.as_view(),
        name="employees-dismissals-check-identity",
    ),
    path(
        "employees-dismissals/<int:id>/",
        views.EmployeesDismissalsDetailsView.as_view(),
        name="employees-dismissals-id",
    ),
]