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
        "deliveries-histories/<int:id>/",
        views.DeliveriesHistoriesDetailsView.as_view(),
        name="deliveries-histories-details",
    ),
    path(
        "deliveries-histories/sync/",
        views.DeliveriesHistoriesSyncView.as_view(),
        name="deliveries-histories-sync",
    ),
    path(
        "deliveries-histories/nf/<str:nf>/",
        views.DeliveriesHistoriesQueriesNFView.as_view(),
        name="deliveries-histories-nf",
    ),
]
