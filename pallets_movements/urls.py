from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.PalletsMovementsView.as_view(),
        name="pallets-movements",
    ),
    path(
        "confirm/<int:id>/",
        views.PalletsMovementsDetailView.as_view(),
        name="pallets-movements-confirm-id",
    ),
    path(
        "document/<int:id>/",
        views.DocumentView.as_view(),
        name="pallets-movements-document-id",
    ),
]
