from django.urls import path

from . import views

urlpatterns = [
    # path(
    #     "",
    #     views.PurchasesEntriesView.as_view(),
    #     name="employees-epis",
    # ),
    path(
        "<int:employee_id>/",
        views.EmployeesEPIsDetailView.as_view(),
        name="employees-epis-employee_id",
    ),
]
