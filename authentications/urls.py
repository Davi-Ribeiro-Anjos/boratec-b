from django.urls import path

from . import views

urlpatterns = [
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
