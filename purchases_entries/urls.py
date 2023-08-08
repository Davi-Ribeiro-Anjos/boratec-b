from django.urls import path

from . import views

urlpatterns = [
    path(
        "purchases-entries/",
        views.PurchasesEntriesView.as_view(),
        name="purchases-entries",
    ),
    path(
        "purchases-entries/<int:id>/",
        views.PurchasesEntriesDetailView.as_view(),
        name="purchases-entries-id",
    ),
]
