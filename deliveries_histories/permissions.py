from rest_framework import permissions
from rest_framework.views import Request, View
from django.db.models import Q


class NFPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.user.groups.filter(Q(name="nf")).exists()
            or request.user.is_superuser
            or request.user.is_staff
        )


class BasePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.user.groups.filter(
                Q(name="delivery_history") | Q(name="delivery_history_admin")
            ).exists()
            or request.user.is_superuser
            or request.user.is_staff
        )


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method == "POST" or request.method == "PATCH":
            return (
                request.user.groups.filter(name="delivery_history_admin").exists()
                or request.user.is_superuser
                or request.user.is_staff
            )

        return (
            request.user.groups.filter(name="delivery_history").exists()
            or request.user.is_superuser
            or request.user.is_staff
        )
