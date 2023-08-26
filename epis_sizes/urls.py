from django.urls import path

from . import views

urlpatterns = [
    path(
        "epis/sizes/",
        views.EPIsSizesView.as_view(),
        name="epis-sizes",
    ),
]
