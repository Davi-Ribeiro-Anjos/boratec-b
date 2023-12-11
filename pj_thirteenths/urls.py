from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.PJThirteenthsView.as_view(),
        name="pj-thirteenths",
    ),
    path(
        "<int:id>/",
        views.PJThirteenthsDetailView.as_view(),
        name="pj-thirteenths-id",
    ),
    path(
        "send/",
        views.PJThirteenthsSendView.as_view(),
        name="pj-thirteenths-send",
    ),
]
