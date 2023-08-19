from django.urls import path

from . import views

urlpatterns = [
    # path(
    #     "employees-epis/",
    #     views.PurchasesEntriesView.as_view(),
    #     name="employees-epis",
    # ),
    path(
        "employees-epis/<int:id>/",
        views.EmployeesEPIsDetailView.as_view(),
        name="employees-epis-id",
    ),
]
