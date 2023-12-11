from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.XmlsView.as_view(),
        name="xmls",
    ),
    path(
        "send/",
        views.XmlsSendView.as_view(),
        name="xmls-send",
    ),
    path(
        "sync/",
        views.XmlsSyncView.as_view(),
        name="xmls-sync",
    ),
    path(
        "download/",
        views.XmlsDownloadView.as_view(),
        name="xmls-download",
    ),
]
