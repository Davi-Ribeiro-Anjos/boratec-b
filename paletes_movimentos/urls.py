from django.urls import path

from . import views

urlpatterns = [
    path(
        "paletes-movimentos/",
        views.PaletesMovimentosView.as_view(),
        name="paletes-movimentos",
    ),
    path(
        "paletes-movimentos/<int:id>/",
        views.PaletesMovimentosDetailView.as_view(),
        name="paletes-movimentos-id",
    ),
]
