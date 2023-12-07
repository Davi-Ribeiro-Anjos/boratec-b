from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.PurchasesRequestsView.as_view(),
        name="purchases-requests",
    ),
    path(
        "<int:id>/",
        views.PurchasesRequestsDetailView.as_view(),
        name="purchases-requests-id",
    ),
]
