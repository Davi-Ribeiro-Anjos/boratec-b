from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.VehiclesView.as_view(),
        name="vehicles",
    ),
]
