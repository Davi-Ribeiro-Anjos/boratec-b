from django.urls import path

from . import views

urlpatterns = [
    path(
        "clientes/",
        views.ClientesView.as_view(),
        name="clientes",
    ),
    path(
        "clientes/documento/<int:id>/",
        views.DocumentoView.as_view(),
        name="clientes-documento-id",
    ),
    path(
        "clientes/choices/",
        views.ClientesChoicesView.as_view(),
        name="clientes-choices",
    ),
]
