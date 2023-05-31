from django.urls import path

from . import views

urlpatterns = [
    path(
        "solicitacoes-entradas/",
        views.SolicitacoesEntradasView.as_view(),
        name="solicitacoes-entradas",
    ),
    path(
        "solicitacoes-entradas/<int:id>/",
        views.SolicitacoesEntradasDetailView.as_view(),
        name="solicitacoes-entradas-id",
    ),
]
