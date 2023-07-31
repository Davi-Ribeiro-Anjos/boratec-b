from rest_framework import permissions
from rest_framework.views import Request, View


class BasePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.user.groups.filter(name="solic_compras").exists()
            or request.user.is_superuser
            or request.user.is_staff
        )


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.user.groups.filter(name="solic_compras_admin").exists()
            or request.user.is_superuser
            or request.user.is_staff
        )
