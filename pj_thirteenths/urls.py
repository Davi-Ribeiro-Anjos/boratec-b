from django.urls import path

from . import views

urlpatterns = [
    path(
        "pj/thirteenths/",
        views.PJThirteenthsView.as_view(),
        name="pj-thirteenths",
    ),
    path(
        "pj/thirteenths/<int:id>/",
        views.PJThirteenthsDetailView.as_view(),
        name="pj-thirteenths-id",
    ),
    path(
        "pj/thirteenths/send/",
        views.PJThirteenthsSendView.as_view(),
        name="pj-thirteenths-send",
    ),
]
