from django.urls import path

from . import views

urlpatterns = [
    path(
        "xmls/",
        views.XmlsView.as_view(),
        name="xmls",
    ),
    path(
        "xmls/send/",
        views.XmlsSendView.as_view(),
        name="xmls-send",
    ),
    path(
        "xmls/sync/",
        views.XmlsSyncView.as_view(),
        name="xmls-sync",
    ),
    path(
        "xmls/download/",
        views.XmlsDownloadView.as_view(),
        name="xmls-download",
    ),
]
