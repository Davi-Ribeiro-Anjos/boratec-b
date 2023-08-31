from django.urls import path

from . import views

urlpatterns = [
    path(
        "epis/sizes/",
        views.EPIsSizesView.as_view(),
        name="epis-sizes",
    ),
    path(
        "epis/sizes/<int:id>/",
        views.EPIsSizesDetailsView.as_view(),
        name="epis-sizes-id",
    ),
]
