from django.urls import path

from . import views

urlpatterns = [
    path(
        "pj-contratos/",
        views.PJContratosView.as_view(),
        name="pj-contratos",
    ),
    path(
        "pj-contratos/<int:id>/",
        views.PJContratosDetailView.as_view(),
        name="pj-contrato-id",
    ),
]
