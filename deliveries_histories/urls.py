from django.urls import path

from . import views

urlpatterns = [
    path(
        "deliveries-histories/",
        views.DeliveriesHistoriesView.as_view(),
        name="deliveries-histories",
    ),
    path(
        "deliveries-histories/confirm/",
        views.DeliveriesHistoriesConfirmedView.as_view(),
        name="deliveries-histories-confirmed",
    ),
    path(
        "deliveries-histories/consult/",
        views.DeliveriesHistoriesConsultView.as_view(),
        name="deliveries-histories-consult",
    ),
    path(
        "deliveries-histories/consult/export/",
        views.DeliveriesHistoriesExportView.as_view(),
        name="deliveries-histories-consult-export",
    ),
    path(
        "deliveries-histories/<int:id>/",
        views.DeliveriesHistoriesDetailsView.as_view(),
        name="deliveries-histories-details",
    ),
    path(
        "deliveries-histories/nf/<str:nf>/",
        views.DeliveriesHistoriesQueriesNFView.as_view(),
        name="deliveries-histories-nf",
    ),
]
