from django.urls import path

from . import views

urlpatterns = [
    path(
        "epis/carts/",
        views.EPIsCartsView.as_view(),
        name="epis-carts",
    ),
]
