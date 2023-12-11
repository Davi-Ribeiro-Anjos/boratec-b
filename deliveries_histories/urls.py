from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.DeliveriesHistoriesView.as_view(),
        name="deliveries-histories",
    ),
    path(
        "confirm/",
        views.DeliveriesHistoriesConfirmedView.as_view(),
        name="deliveries-histories-confirmed",
    ),
    path(
        "performance/",
        views.DeliveriesHistoriesPerformanceView.as_view(),
        name="deliveries-histories-performance",
    ),
    path(
        "performance/export/",
        views.DeliveriesHistoriesExportView.as_view(),
        name="deliveries-histories-performance-export",
    ),
    path(
        "status/",
        views.DeliveriesHistoriesStatusView.as_view(),
        name="deliveries-histories-status",
    ),
    path(
        "status/export/",
        views.DeliveriesHistoriesStatusExportView.as_view(),
        name="deliveries-histories-status-export",
    ),
    path(
        "<int:id>/",
        views.DeliveriesHistoriesDetailsView.as_view(),
        name="deliveries-histories-details",
    ),
    path(
        "nf/<str:nf>/",
        views.DeliveriesHistoriesQueriesNFView.as_view(),
        name="deliveries-histories-nf",
    ),
]
