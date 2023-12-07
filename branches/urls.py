from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.BranchesView.as_view(),
        name="branches",
    ),
]
