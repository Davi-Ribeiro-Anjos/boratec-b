from django.urls import path

from . import views

urlpatterns = [
    path(
        "epis/requests/",
        views.EPIsRequestsView.as_view(),
        name="epis-requests",
    ),
    path(
        "epis/requests/cancel/<int:id>/",
        views.EPIsRequestsCancelView.as_view(),
        name="epis-requests-cancel",
    ),
    path(
        "epis/requests/<int:id>/",
        views.EPIsRequestsDetailsView.as_view(),
        name="epis-requests-id",
    ),
]
