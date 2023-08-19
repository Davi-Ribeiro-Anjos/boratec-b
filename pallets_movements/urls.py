from django.urls import path

from . import views

urlpatterns = [
    path(
        "pallets-movements/",
        views.PalletsMovementsView.as_view(),
        name="pallets-movements",
    ),
    path(
        "pallets-movements/confirm/<int:id>/",
        views.PalletsMovementsDetailView.as_view(),
        name="pallets-movements-confirm-id",
    ),
    path(
        "pallets-movements/document/<int:id>/",
        views.DocumentView.as_view(),
        name="pallets-movements-document-id",
    ),
]
