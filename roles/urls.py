from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.RolesView.as_view(),
        name="roles",
    ),
]
