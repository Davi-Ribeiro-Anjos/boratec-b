from django.urls import path

from . import views

urlpatterns = [
    path(
        "paletes-controles/",
        views.PaletesControlesView.as_view(),
        name="paletes-controles",
    )
]
