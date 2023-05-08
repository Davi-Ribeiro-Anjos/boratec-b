from django.urls import path

from . import views

urlpatterns = [
    path(
        "filiais/",
        views.FiliaisView.as_view(),
        name="filiais",
    ),
]
