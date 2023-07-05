from django.urls import path

from . import views

urlpatterns = [
    path(
        "usuarios/",
        views.UsuariosView.as_view(),
        name="usuarios",
    ),
]
