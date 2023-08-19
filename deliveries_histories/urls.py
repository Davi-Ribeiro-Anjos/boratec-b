from django.urls import path

from . import views

urlpatterns = [
    path(
        "deliveries-histories/nf/<str:nf>/",
        views.DeliveriesHistoriesQueriesNFView.as_view(),
        name="deliveries-histories-nf",
    ),
]
