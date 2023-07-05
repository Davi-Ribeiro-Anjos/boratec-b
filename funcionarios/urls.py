from django.urls import path

from . import views

urlpatterns = [
    path(
        "funcionarios/",
        views.FuncionariosView.as_view(),
        name="funcionarios",
    ),
    path(
        "funcionarios/<int:id>/",
        views.FuncionariosDetailView.as_view(),
        name="funcionarios-id",
    ),
    path(
        "funcionarios/choices/",
        views.FuncionariosChoicesView.as_view(),
        name="funcionarios-choices",
    ),
]
