from rest_framework import permissions
from rest_framework.views import Request, View
from django.db.models import Q


class BasePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.user.groups.filter(
                Q(name="pallet_client") | Q(name="pallet_client_admin")
            ).exists()
            or request.user.is_superuser
            or request.user.is_staff
        )


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method == "POST":
            return (
                request.user.groups.filter(name="pallet_client_admin").exists()
                or request.user.is_superuser
                or request.user.is_staff
            )

        return (
            request.user.groups.filter(name="pallet_client").exists()
            or request.user.is_superuser
            or request.user.is_staff
        )
