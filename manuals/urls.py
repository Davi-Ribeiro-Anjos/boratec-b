from django.urls import path

from . import views

urlpatterns = [
    path(
        "queries/manuals/",
        views.ManualsView.as_view(),
        name="queries-manuals",
    ),
    path(
        "queries/manuals/<int:id>/",
        views.ManualsDetailsView.as_view(),
        name="queries-manuals-id",
    ),
]
