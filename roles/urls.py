from django.urls import path

from . import views

urlpatterns = [
    path(
        "roles/",
        views.RolesView.as_view(),
        name="roles",
    ),
]
