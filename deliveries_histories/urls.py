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
        "deliveries-histories/performance/",
        views.DeliveriesHistoriesPerformanceView.as_view(),
        name="deliveries-histories-performance",
    ),
    path(
        "deliveries-histories/performance/export/",
        views.DeliveriesHistoriesExportView.as_view(),
        name="deliveries-histories-performance-export",
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
