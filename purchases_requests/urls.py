from django.urls import path

from . import views

urlpatterns = [
    path(
        "purchases-requests/",
        views.PurchasesRequestsView.as_view(),
        name="purchases-requests",
    ),
    path(
        "purchases-requests/<int:id>/",
        views.PurchasesRequestsDetailView.as_view(),
        name="purchases-requests-id",
    ),
]
