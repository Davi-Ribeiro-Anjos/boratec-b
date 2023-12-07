from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.EPIsCartsView.as_view(),
        name="epis-carts",
    ),
]
