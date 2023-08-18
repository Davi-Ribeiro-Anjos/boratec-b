from django.urls import path

from . import views

urlpatterns = [
    path(
        "fleets_availabilities/",
        views.FleetsAvailabilitiesView.as_view(),
        name="fleets_availabilities",
    ),
]
