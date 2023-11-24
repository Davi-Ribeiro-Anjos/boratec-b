from django.urls import path

from . import views

urlpatterns = [
    path(
        "users/",
        views.UsersView.as_view(),
        name="users",
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
    # path(
    #     "forget-password/",
    #     views.ForgetPasswordView.as_view(),
    #     name="forget-password",
    # ),
    # path(
    #     "set-password/<str:email>/<str:token>/",
    #     views.SetPasswordView.as_view(),
    #     name="set-password",
    # ),
]
