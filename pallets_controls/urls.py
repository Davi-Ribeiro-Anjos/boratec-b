from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.PalletsControlsView.as_view(),
        name="pallets-controls",
    )
]
