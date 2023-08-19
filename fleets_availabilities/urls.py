from django.urls import path

from . import views

urlpatterns = [
    path(
        "fleets-availabilities/",
        views.FleetsAvailabilitiesView.as_view(),
        name="fleets-availabilities",
    ),
]
