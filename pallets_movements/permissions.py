from rest_framework import permissions
from rest_framework.views import Request, View
from django.db.models import Q


class BasePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.user.groups.filter(
                Q(name="pallet_branch") | Q(name="pallet_branch_admin")
            ).exists()
            or request.user.is_superuser
            or request.user.is_staff
        )


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method == "PATCH":
            return (
                request.user.groups.filter(name="pallet_branch_admin").exists()
                or request.user.is_superuser
                or request.user.is_staff
            )

        return (
            request.user.groups.filter(name="pallet_branch").exists()
            or request.user.is_superuser
            or request.user.is_staff
        )
