from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.ManualsView.as_view(),
        name="queries-manuals",
    ),
    path(
        "<int:id>/",
        views.ManualsDetailsView.as_view(),
        name="queries-manuals-id",
    ),
]
