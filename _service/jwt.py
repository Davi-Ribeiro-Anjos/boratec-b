import jwt

from _app.settings import SECRET_KEY
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from employees.models import Employees
from employees.serializers import EmployeesLoginSerializer


def custom_payload_handler(token):
    try:
        user_id = token.get("user_id")

        employee = get_object_or_404(Employees, user_id=user_id)

        token["employee"] = dict(EmployeesLoginSerializer(employee).data)

        return jwt.encode(token, SECRET_KEY, algorithm="HS256")
    except Exception:
        return jwt.encode(token, SECRET_KEY, algorithm="HS256")
