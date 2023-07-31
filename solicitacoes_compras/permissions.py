from rest_framework import permissions
from rest_framework.views import Request, View

from django.contrib.auth.models import Group, User
from django.db.models import Q


class HasPermissionByGroup(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        group = Group.objects.filter(
            Q(name="solic_compras") | Q(name="solic_compras_adm")
        )

        return request.user.is_authenticated
