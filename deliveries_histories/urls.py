from django.urls import path

from . import views

urlpatterns = [
    path(
        "deliveries-histories/",
        views.DeliveriesHistoriesView.as_view(),
        name="deliveries-histories",
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
