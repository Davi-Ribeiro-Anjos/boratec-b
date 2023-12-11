from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.PurchasesEntriesView.as_view(),
        name="purchases-entries",
    ),
    path(
        "<int:id>/",
        views.PurchasesEntriesDetailsView.as_view(),
        name="purchases-entries-id",
    ),
]
