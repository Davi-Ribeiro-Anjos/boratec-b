from django.urls import path

from . import views

urlpatterns = [
    path(
        "paletes-movimentos/",
        views.PaletesMovimentosView.as_view(),
        name="paletes-movimentos",
    ),
    path(
        "paletes-movimentos/confirmar/<int:id>/",
        views.PaletesMovimentosDetailView.as_view(),
        name="paletes-movimentos-confirmar-id",
    ),
    path(
        "paletes-movimentos/documento/<int:id>/",
        views.DocumentoView.as_view(),
        name="paletes-movimentos-documento-id",
    ),
]
