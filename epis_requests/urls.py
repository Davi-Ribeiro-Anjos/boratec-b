from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.EPIsRequestsView.as_view(),
        name="epis-requests",
    ),
    path(
        "cancel/<int:id>/",
        views.EPIsRequestsCancelView.as_view(),
        name="epis-requests-cancel",
    ),
    path(
        "<int:id>/",
        views.EPIsRequestsDetailsView.as_view(),
        name="epis-requests-id",
    ),
]
