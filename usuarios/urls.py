from django.urls import path

from . import views

urlpatterns = [
    path(
        "usuarios/",
        views.UsuariosView.as_view(),
        name="usuarios",
    ),
    path(
        "login/",
        views.CustomTokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "refresh/",
        views.CustomTokenRefreshView.as_view(),
        name="refresh",
    ),
]
