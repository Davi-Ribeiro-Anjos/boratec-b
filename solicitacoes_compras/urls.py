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
    path(
        "solicitacoes-compras/choices/",
        views.SolicitacoesComprasChoicesView.as_view(),
        name="solicitacoes-compras-choices",
    ),
]
