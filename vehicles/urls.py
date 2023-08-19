from django.urls import path

from . import views

urlpatterns = [
    path(
        "vehicles/",
        views.VehiclesView.as_view(),
        name="vehicles",
    ),
]
