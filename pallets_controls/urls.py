from django.urls import path

from . import views

urlpatterns = [
    path(
        "pallets-controls/",
        views.PalletsControlsView.as_view(),
        name="pallets-controls",
    )
]
