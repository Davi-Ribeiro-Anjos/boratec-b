from django.urls import path

from . import views

urlpatterns = [
    path(
        "solicitacoes-compras/",
        views.SolicitacoesComprasView.as_view(),
        name="solicitacoes-compras",
    ),
    path(
        "solicitacoes-compras/<int:id>/",
        views.SolicitacoesComprasDetailView.as_view(),
        name="solicitacoes-compras-id",
    ),
]
