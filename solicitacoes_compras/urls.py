from django.urls import path

from . import views

urlpatterns = [
    path(
        "solicitacoes-compras/",
        views.SolicitacoesComprasView.as_view(),
        name="solicitacoes-compras",
    ),
]
