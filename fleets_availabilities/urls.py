from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.FleetsAvailabilitiesView.as_view(),
        name="fleets-availabilities",
    ),
]
