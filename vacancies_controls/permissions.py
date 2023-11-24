from rest_framework import permissions
from rest_framework.views import Request, View
from django.db.models import Q


class MainPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method == "PATCH":
            return (
                request.user.groups.filter(name="employee_vacancy_admin").exists()
                or request.user.is_superuser
                or request.user.is_staff
            )

        return (
            request.user.groups.filter(name="employee_vacancy").exists()
            or request.user.is_superuser
            or request.user.is_staff
        )
